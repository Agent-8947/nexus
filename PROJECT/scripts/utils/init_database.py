import sqlite3
import os
from datetime import datetime

class NexusDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 1. Таблица проектов (Core Projects)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                archetype TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. Таблица ассетов (Documents/Files in E:\ outputs)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT, -- docx, pdf, html
                file_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')

        # 3. Таблица памяти/стека (Memory & State)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nexus_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 4. Лог команд (Command History via Pipes)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                executor TEXT, -- Python, Node, Agent
                result TEXT,
                execution_time_ms REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Инициализация базовых данных
        cursor.execute("INSERT OR IGNORE INTO nexus_state (key, value) VALUES ('archetype', 'AI-Orchestrated-NEXUS-v2')")
        cursor.execute("INSERT OR IGNORE INTO nexus_state (key, value) VALUES ('version', '2026.1')")

        conn.commit()
        conn.close()
        print(f"[*] NEXUS Database initialized at: {self.db_path}")

if __name__ == "__main__":
    PROJECT_ROOT = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT"
    DB_FILE = os.path.join(PROJECT_ROOT, "nexus_optimus.db")
    
    # Создаем директорию если нет (хотя PROJECT должна быть)
    if not os.path.exists(PROJECT_ROOT):
        os.makedirs(PROJECT_ROOT)
        
    db = NexusDatabase(DB_FILE)
