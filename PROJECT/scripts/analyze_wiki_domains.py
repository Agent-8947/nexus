import json
from pathlib import Path

def analyze_wiki():
    brain_path = Path(r'e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\nexus_global_brain.json')
    if not brain_path.exists():
        print(f"Error: {brain_path} not found.")
        return

    with open(brain_path, encoding='utf-8') as f:
        data = json.load(f)

    stats = {
        'OSINT': [],
        'LEGAL': [],
        'OSINT_LEGAL_CROSS': [],
        'MACHINE_LEARNING': [],
        'CRYPTO': [],
        'ROBOTICS': []
    }

    for name, item in data.items():
        domains = item.get('domains', [])
        is_osint = 'OSINT' in domains
        is_legal = 'LEGAL' in domains
        
        if is_osint and is_legal:
            stats['OSINT_LEGAL_CROSS'].append(name)
        elif is_osint:
            stats['OSINT'].append(name)
        elif is_legal:
            stats['LEGAL'].append(name)
            
        if 'MACHINE_LEARNING' in domains:
            stats['MACHINE_LEARNING'].append(name)
        if 'CRYPTO' in domains:
            stats['CRYPTO'].append(name)
        if 'ROBOTICS' in domains:
            stats['ROBOTICS'].append(name)

    print(f"\n--- WIKI DOMAIN ANALYSIS ---")
    print(f"Total entries: {len(data)}")
    print(f"OSINT only: {len(stats['OSINT'])}")
    print(f"LEGAL only: {len(stats['LEGAL'])}")
    print(f"OSINT + LEGAL cross-domain: {len(stats['OSINT_LEGAL_CROSS'])}")
    print(f"Machine Learning: {len(stats['MACHINE_LEARNING'])}")
    print(f"Crypto: {len(stats['CRYPTO'])}")
    print(f"Robotics: {len(stats['ROBOTICS'])}")
    
    print(f"\nTOP CROSS-DOMAIN TOOLS (Legal-OSINT):")
    for tool in stats['OSINT_LEGAL_CROSS'][:20]:
        print(f"- {tool}")

if __name__ == "__main__":
    analyze_wiki()
