import sys
import os
import datetime
import uuid

def log_idea(content):
    idea_dir = "PROJECT/IDEA"
    log_file = os.path.join(idea_dir, "LOG.md")
    
    if not os.path.exists(idea_dir):
        os.makedirs(idea_dir)
        
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    idea_id = str(uuid.uuid4())[:8].upper()
    
    entry = f"\n---\n### 💡 ID: {idea_id} | {timestamp}\n{content}\n"
    
    file_exists = os.path.exists(log_file)
    with open(log_file, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("# 🧠 NEXUS IDEA LOG\n\nРеестр стратегических идей и архитектурных гипотез.\n")
        f.write(entry)
    
    print(f"[+] Idea {idea_id} captured and safely stored in PROJECT/IDEA/LOG.md")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        log_idea(" ".join(sys.argv[1:]))
    else:
        print("[-] Error: No idea content provided.")
        sys.exit(1)
