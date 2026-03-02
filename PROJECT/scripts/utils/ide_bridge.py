import os
import json
import time

# NEXUS IDE BRIDGE (Proactive Agent Interface)
# Этот скрипт служит интерфейсом для запроса LLM-мощностей непосредственно у агента IDE (Gemini).

class IDEBridge:
    def __init__(self, task_file=".nexus_task.json", resp_file=".nexus_response.json"):
        self.root = "e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT"
        self.task_path = os.path.join(self.root, task_file)
        self.resp_path = os.path.join(self.root, resp_file)

    def request_llm(self, task_type, payload):
        """
        Отправляет запрос агенту IDE через файловый триггер.
        """
        print(f"📡 IDE Bridge: Requesting {task_type} from IDE Agent...")
        
        task_data = {
            "type": task_type,
            "payload": payload,
            "timestamp": time.time(),
            "status": "PENDING"
        }
        
        # 1. Записываем задачу
        with open(self.task_path, "w", encoding="utf-8") as f:
            json.dump(task_data, f, indent=4)
            
        print("⏳ Waiting for IDE Agent response (Gemini)...")
        
        # 2. Ожидаем ответа (таймаут 60 сек)
        start_time = time.time()
        while time.time() - start_time < 60:
            if os.path.exists(self.resp_path):
                try:
                    with open(self.resp_path, "r", encoding="utf-8") as f:
                        resp = json.load(f)
                        
                    # Проверяем, что ответ к нашему таску
                    if resp.get("status") == "COMPLETED" and resp.get("timestamp", 0) > task_data["timestamp"]:
                        print("✅ IDE Agent response received!")
                        # Удаляем файлы после завершения
                        os.remove(self.task_path)
                        os.remove(self.resp_path)
                        return resp.get("result")
                except:
                    pass
            time.sleep(1)
            
        print("❌ IDE Bridge Timeout: No response from agent.")
        return None

if __name__ == "__main__":
    # Test call
    bridge = IDEBridge()
    # bridge.request_llm("test", "Hello from NEXUS!")
