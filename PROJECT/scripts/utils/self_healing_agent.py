import os
import subprocess
import sys
import tempfile
import time

# Если мы хотим использовать паттерны LangGraph, нам нужны промпты и цепочки
# Для этого примера мы реализуем автономный "Self-Healing Loop"

class SelfHealingAgent:
    def __init__(self, api_key=None, max_retries=3):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.max_retries = max_retries
        
    def run_and_fix(self, script_path):
        print(f"🛠️ Starting Self-Healing process for: {script_path}")
        
        for attempt in range(1, self.max_retries + 1):
            print(f"🔄 Attempt {attempt}/{self.max_retries}...")
            
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Success! Script executed successfully on attempt {attempt}.")
                return True
            
            print(f"❌ Execution failed with error:\n{result.stderr}")
            
            if not self.api_key:
                print("⚠️ No ANTHROPIC_API_KEY found. Self-healing aborted.")
                return False
                
            if attempt == self.max_retries:
                print("🛑 Max retries reached. Failing.")
                return False
                
            print("🚀 Asking AI for a fix...")
            fix = self._get_ai_fix(script_path, result.stderr)
            
            if fix:
                print("💾 Applying AI fix...")
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(fix)
                time.sleep(1) # Короткая пауза перед ретраем
            else:
                print("❌ AI failed to provide a fix.")
                return False
                
        return False

    def _get_ai_fix(self, script_path, error_msg):
        """
        Requesting a fix through the IDE Bridge (Native Gemini).
        """
        try:
            from ide_bridge import IDEBridge
            bridge = IDEBridge()
            
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            payload = {
                "script": content,
                "error": error_msg,
                "instruction": "Fix the provided Python script to resolve the execution error. Return ONLY raw code."
            }
            
            # Делегируем запрос агенту IDE (Gemini)
            fix_content = bridge.request_llm("FIX_CODE", payload)
            
            if fix_content:
                # Очистка от маркдауна если пришел от Gemini
                if "```python" in fix_content:
                    fix_content = fix_content.split("```python")[1].split("```")[0].strip()
                elif fix_content.startswith("```"):
                    fix_content = fix_content.split("```")[1].strip()
                    
                return fix_content
            
            # Fallback к старой логике (если есть ключ)
            if self.api_key:
                from anthropic import Anthropic
                print("⚠️ IDE Bridge failed. Falling back to Anthropic...")
                client = Anthropic(api_key=self.api_key)
                # ... (старый код с Anthropic Claude)
                pass

            return None
            
        except Exception as e:
            print(f"❌ AI Fix Error: {e}")
            return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python self_healing_agent.py <script_to_fix.py>")
        sys.exit(1)
        
    sh_agent = SelfHealingAgent()
    sh_agent.run_and_fix(sys.argv[1])
