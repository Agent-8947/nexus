import os
import json
import time
import glob
import shutil
import subprocess
import sys

# --- CONFIGURATION ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
OUTPUT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/cmd_output.json"))

# 🗺 NEXUS DELEGATION MAP
# Сопоставление команд с новыми агентскими скриптами
AGENT_MAP = {
    "RUN_AUDIT": "scripts/office/run_lighthouse_audit.py",
    "RUN_GEO": "scripts/office/run_geo_analysis.py",
    "SELF_HEAL": "scripts/utils/self_healing_agent.py",
    "GEN_MARKETING": "scripts/office/generate_marketing_kit.py",
    "PLAN_TASK": "scripts/utils/plan_and_execute_orchestrator.py",
    "DOC_GEN": "scripts/office/DocumentFactory.py",
    "MCP": "scripts/utils/mcp_launcher.py"
}

# Инициализация Launcher
try:
    from mcp_launcher import MCPLauncher
    mcp_launcher = MCPLauncher()
except:
    mcp_launcher = None

def scan_todos():
    """Scans project for TODO and FIXME tags."""
    todos = []
    extensions = ['*.py', '*.js', '*.html', '*.md', '*.astro']
    for ext in extensions:
        files = glob.glob(os.path.join(PROJECT_ROOT, "**", ext), recursive=True)
        for f_path in files:
            if any(x in f_path for x in ["node_modules", ".venv", ".git"]): continue
            try:
                with open(f_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if "TODO" in line or "FIXME" in line:
                            clean_line = line.strip().replace('"', "'")
                            todos.append(f"{os.path.basename(f_path)}:L{i+1} -> {clean_line}")
            except: continue
    return todos

def clean_junk():
    """Removes pycache and temporary files."""
    count = 0
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for d in dirs:
            if d == "__pycache__":
                try:
                    shutil.rmtree(os.path.join(root, d))
                    count += 1
                except: pass
    return f"Cleaned {count} cache directories."

def delegate_to_agent(agent_key, target=None):
    """
    Supervision Logic: Delegates task to a specialized agent script.
    """
    if agent_key not in AGENT_MAP:
        return {"status": "ERROR", "msg": f"Agent {agent_key} not found."}
    
    script_path = os.path.join(PROJECT_ROOT, AGENT_MAP[agent_key])
    if not os.path.exists(script_path):
        return {"status": "ERROR", "msg": f"Script missing at {script_path}"}
    
    print(f"[Supervisor] Delegating '{agent_key}' to sub-agent...")
    command = [sys.executable, script_path]
    if target: command.append(target)
    
    try:
        # Запускаем в фоне или ждем? Для диспетчера лучше ждать краткие задачи
        res = subprocess.run(command, capture_output=True, text=True, timeout=120)
        return {
            "status": "SUCCESS" if res.returncode == 0 else "FAILED",
            "msg": f"Agent {agent_key} finished execution.",
            "data": res.stdout.splitlines()[-10:] # Последние 10 строк логов
        }
    except Exception as e:
        return {"status": "ERROR", "msg": f"Delegation failed: {str(e)}"}

def process_cmd(raw_data):
    """
    NEXUS Supervisor: The Main Orchestrator Logic.
    """
    try:
        # Парсим вход (может быть строкой COMMAND или JSON {"cmd": "", "arg": ""})
        arg = None
        if isinstance(raw_data, bytes): raw_data = raw_data.decode()
        
        try:
            data_json = json.loads(raw_data)
            cmd = data_json.get("cmd", "").upper()
            arg = data_json.get("arg")
        except:
            cmd = raw_data.strip().upper()

        print(f"[Supervisor] Command Received: {cmd} (Arg: {arg})")
        result = {"status": "VOID", "data": [], "timestamp": time.time()}
        
        # 1. Base Commands
        if cmd == "SCAN_TODO":
            results = scan_todos()
            result.update({"status": "SUCCESS", "msg": f"Found {len(results)} items", "data": results})
        
        elif cmd == "SYS_INFO":
            import psutil
            cpu, mem = psutil.cpu_percent(), psutil.virtual_memory().percent
            result.update({"status": "SUCCESS", "msg": f"CPU: {cpu}% | RAM: {mem}%", "data": [f"CPU: {cpu}%", f"RAM: {mem}%"]})
            
        elif cmd == "SYS_CLEAN":
            msg = clean_junk()
            result.update({"status": "SUCCESS", "msg": msg})
            
        # 2. Agent Delegation
        elif cmd in AGENT_MAP:
            res = delegate_to_agent(cmd, arg)
            result.update(res)
            
        else:
            result.update({"status": "UNKNOWN", "msg": f"Command '{cmd}' not recognized."})

        # Save result for persistent state
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)
            
        return result
        
    except Exception as e:
        error_res = {"status": "ERROR", "msg": str(e), "timestamp": time.time()}
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(error_res, f)
        return error_res

