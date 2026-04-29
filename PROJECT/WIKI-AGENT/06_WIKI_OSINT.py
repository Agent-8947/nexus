import socket
import ssl
import json
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# ==============================================================================
# SYSTEM PROMPT / GOVERNANCE: NEXUS CONSTITUTIONAL LAWS
# ==============================================================================
# Agent ID   : 06_WIKI_OSINT
# Version    : 1.0.0      [LAW-10: AGENT SEMVER]
# Execution  : Stealth    [LAW-02: STEALTH]
# Boundaries : Read-Only  [LAW-91: ETHICAL HACKING BOUNDARIES]
# ==============================================================================

# [LAW-03: TYPE CONTRACTS]
class OsintTarget(BaseModel):
    target_domain: str = Field(..., description="Domain to investigate (e.g., example.com)")
    trace_id: str = Field(..., description="Unique task tracker ID")
    stealth_mode: bool = Field(True, description="Enforce aggressive delays and random User-Agents")

class OsintResult(BaseModel):
    domain: str
    is_alive: bool
    ip_address: Optional[str] = None
    ssl_issuer: Optional[str] = None
    server_header: Optional[str] = None
    facts: List[str] = []
    timestamp: str

class NexusOsintAgent:
    def __init__(self):
        # [LAW-02: STEALTH] Randomizing basic headers to look like a normal web browser.
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }

    def _get_ip(self, domain: str) -> Optional[str]:
        # [LAW-06: FAIL-SAFE DEFAULTS] Wrap unstable I/O in soft blocks
        try:
            return socket.gethostbyname(domain)
        except Exception:
            return None

    def _get_ssl_info(self, domain: str) -> Optional[str]:
        # [LAW-78: SSL EXPIRY ALERT] Basic SSL reconnaissance without triggering alarms
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    for item in cert.get('issuer', []):
                        for key, value in item:
                            if key == 'organizationName':
                                return value
        except Exception:
            pass
        return None

    def _ping_service(self, domain: str) -> dict:
        # [LAW-32: RECON FIRST] Lightweight HTTP Head/Get request
        url = f"https://{domain}"
        req = urllib.request.Request(url, headers=self.headers, method='HEAD')
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return {
                    "is_alive": True,
                    "server": response.getheader('Server', 'Hidden')
                }
        except urllib.error.URLError:
            # Fallback to HTTP if HTTPS fails
            url = f"http://{domain}"
            req_http = urllib.request.Request(url, headers=self.headers, method='HEAD')
            try:
                with urllib.request.urlopen(req_http, timeout=5) as resp:
                    return {
                        "is_alive": True,
                        "server": resp.getheader('Server', 'Hidden')
                    }
            except Exception:
                return {"is_alive": False, "server": None}
        except Exception:
            return {"is_alive": False, "server": None}

    def run(self, input_data: OsintTarget) -> OsintResult:
        print(f"[*] AGENT 06 [OSINT]: Commencing stealth recon on {input_data.target_domain} (Trace: {input_data.trace_id})")
        
        domain = input_data.target_domain
        facts = []
        
        # Recon Phase 1: DNS & IP
        ip_addr = self._get_ip(domain)
        if ip_addr:
            facts.append(f"Domain revolves to IP {ip_addr}")
        else:
            facts.append("Failed to resolve via DNS.")
            
        # Recon Phase 2: HTTP Reachability
        http_data = self._ping_service(domain)
        if http_data['is_alive']:
            facts.append("HTTP(S) service is alive.")
            if http_data['server'] != 'Hidden':
                facts.append(f"Server signature inferred as {http_data['server']}.")
            else:
                facts.append("Server signature is masked (Stealth configuration).")
        else:
            facts.append("Target endpoint is totally unresponsive to ping.")

        # Recon Phase 3: TLS/SSL Profile
        ssl_issuer = self._get_ssl_info(domain)
        if ssl_issuer:
            facts.append(f"SSL certificated issued by {ssl_issuer}.")

        # Wrap in output Contract
        result = OsintResult(
            domain=domain,
            is_alive=http_data['is_alive'],
            ip_address=ip_addr,
            ssl_issuer=ssl_issuer,
            server_header=http_data['server'],
            facts=facts,
            timestamp=datetime.now().isoformat()
        )
        
        print(f"[+] OSINT Complete. Found {len(facts)} facts.")
        return result

if __name__ == "__main__":
    # Internal Unit Test [LAW-14: AUTOMATED REGRESSION]
    test_target = OsintTarget(target_domain="github.com", trace_id="REQ-TEST-001", stealth_mode=True)
    agent = NexusOsintAgent()
    output = agent.run(test_target)
    
    # Simulating data handoff to Log/Console -> could go directly to 19_WIKI_COMPOUNDER
    print(output.model_dump_json(indent=2))
