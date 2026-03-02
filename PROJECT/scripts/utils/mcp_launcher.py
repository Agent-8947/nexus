import os
import json
import subprocess
import sys

# NEXUS MCP LAUNCHER
# Этот скрипт управляет запуском эталонных MCP серверов.

class MCPLauncher:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.join("e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT", "mcp_config.json")
        self.active_processes = {}

    def start_server(self, server_name):
        """
        Запускает MCP сервер на основе конфигурации.
        """
        print(f"🚀 Launching MCP Server: {server_name}...")
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        server_cfg = config.get("mcpServers", {}).get(server_name)
        if not server_cfg:
            print(f"❌ Server '{server_name}' not found in config.")
            return False
            
        cmd = [server_cfg["command"]] + server_cfg["args"]
        
        # Инъекция переменных окружения
        env = os.environ.copy()
        
        # 1. Загружаем из config (если прописаны)
        cfg_env = server_cfg.get("env", {})
        env.update(cfg_env)
        
        # 2. Попытка загрузить из .env.mcp (более безопасно)
        env_mcp = self.config_path.replace("mcp_config.json", ".env.mcp")
        if os.path.exists(env_mcp):
            try:
                from dotenv import load_dotenv, main
                user_env = main.dotenv_values(env_mcp)
                env.update(user_env)
                print(f"🔑 Loaded secrets from {os.path.basename(env_mcp)}")
            except: pass

        # Мы используем Popen, чтобы сервер работал в фоне
        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                env=env # Передаем токены в процесс сервера
            )
            self.active_processes[server_name] = process
            print(f"✅ Server '{server_name}' started (PID: {process.pid})")
            return True
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False

    def list_servers(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return list(config.get("mcpServers", {}).keys())

    def stop_all(self):
        for name, proc in self.active_processes.items():
            print(f"🛑 Stopping {name}...")
            proc.terminate()

if __name__ == "__main__":
    launcher = MCPLauncher()
    if len(sys.argv) > 1:
        launcher.start_server(sys.argv[1])
    else:
        print(f"Available servers: {launcher.list_servers()}")
