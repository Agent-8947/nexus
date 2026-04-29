import os
import re
import shutil
from pathlib import Path

DNA_DIR = Path(__file__).resolve().parent

CATEGORIES = {
    "DNA_OSINT": ['osint', 'crawler', 'spiderfoot', 'rapidscan', 'autosploit', 'gitleaks', 'appinfoscanner', 'chipsec', 'exploit', 'crawl4ai', 'recon', 'threat', 'patrol', 'metasploit', 'vuln', 'malware', 'security', 'hardening', 'oracle', 'godeye'],
    "DNA_WEB": ['video', 'presenter', 'motion', 'gsap', 'threejs', 'ui', 'tailwind', 'css', 'design', 'recorder', 'animation', 'render', '3d', 'nuxt', 'vue', 'hugo', 'umami', 'canvas', 'motion_recorder'],
    "DNA_AI_ML": ['ai', 'ml', 'machine_learning', 'deep_learning', 'nlp', 'pytorch', 'keras', 'stanford', 'detectron', 'neural', 'vision_to_prompt', 'transformer', 'learning', 'dataset', 'algorithm', 'math', 'forecast'],
    "DNA_HARDWARE": ['slam', 'fpga', 'lidar', 'uav', 'drone', 'esp32', 'ros', 'baremetal', 'hardware', 'embedded', 'robotic', 'calibration', 'spatial', 'depth', 'lunar'],
    "DNA_INFRA": ['infrastructure', 'infra', 'devops', 'airflow', 'alluxio', 'grafana', 'proxy', 'frp', 'agenix', 'linux', 'ohmyzsh', 'ha-proxy', 'wireguard', 'baremetal-os', 'sys', 'architect', 'docker', 'vault', 'borg', 'bucket4j'],
    "DNA_SECURITY_ADV": ['pentest', 'rootkit', 'chaos', 'crypt', 'zen', 'gpg', 'bearer', 'audit', 'seal'],
    "DNA_SYNTH_TOOLS": ['backoff', 'spacedrive', 'socket.io', 'nanochat', 'ladybird', 'libpointmatcher', 'dotenv', 'spiffs', 'linfa', 'evidence', 'troubleshooting', 'r4ds', '30-days-of-python', 'master_evolver', 'viz_engine']
}

def sort_and_number_agent(agent_file: Path) -> Path:
    """Categorizes and renumbers the agent file based on its type and current folder state."""
    name_low = agent_file.name.lower()
    target_folder_name = "DNA_SYNTH_TOOLS" # Default
    
    # Check OSINT first
    for cat_name, keywords in CATEGORIES.items():
        if any(k in name_low for k in keywords):
            target_folder_name = cat_name
            break

    target_dir = DNA_DIR / target_folder_name
    target_dir.mkdir(exist_ok=True, parents=True)

    # Determine next number
    files = [f for f in os.listdir(target_dir) if f.endswith('.py')]
    max_num = 0
    for f in files:
        match = re.match(r'^(\d+)_', f)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    
    next_num = max_num + 1
    
    # Final Rename and Move
    clean_name = re.sub(r'^\d+_', '', agent_file.name)
    final_name = f"{next_num:02d}_{clean_name}"
    final_path = target_dir / final_name
    
    shutil.move(str(agent_file), str(final_path))
    return final_path
