import subprocess
import os
import sys
import json
from datetime import datetime

def run_audit(url="http://localhost:4321"):
    print(f"🚀 Starting Lighthouse Audit for: {url}")
    
    output_dir = os.path.join("e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT", "outputs", "audits")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"audit_{timestamp}.json")
    
    # Команда для запуска site-audit-seo
    # Мы используем npx для запуска без предварительной установки
    command = [
        "npx", "-y", "site-audit-seo", 
        url, 
        "--headless", 
        "--lighthouse",
        "--upload"
    ]
    
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        
        full_output = ""
        for line in process.stdout:
            print(line, end="")
            full_output += line
            
        process.wait()
        
        if process.returncode == 0:
            print(f"\n✅ Audit complete! Report saved locally.")
            # Попытаться извлечь ссылку на выгруженный отчет из вывода
            if "Public report link:" in full_output:
                link = full_output.split("Public report link:")[1].split("\n")[0].strip()
                print(f"🔗 Public Report: {link}")
                
            # Сохраняем логи в файл
            with open(os.path.join(output_dir, f"audit_log_{timestamp}.txt"), "w", encoding="utf-8") as f:
                f.write(full_output)
                
            return True
        else:
            print(f"\n❌ Audit failed with exit code {process.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running audit: {e}")
        return False

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4321"
    run_audit(target_url)
