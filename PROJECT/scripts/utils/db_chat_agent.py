import sqlite3
import os
import sys
import json

# DB Chat Agent: Позволяет общаться с базой данных nexus_optimus.db
class DBChatAgent:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join("e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT", "nexus_optimus.db")
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")

    def query(self, nl_text):
        """
        Преобразует естественный язык в SQL (если есть API ключ) или выполняет SQL.
        """
        print(f"🗄 DB Search: {nl_text}")
        
        if not os.path.exists(self.db_path):
            return {"status": "ERROR", "msg": "Database file not found."}
            
        sql = nl_text # По умолчанию считаем, что пришел SQL
        
        # Переключение на AI если это текст
        if not nl_text.strip().upper().startswith(("SELECT", "INSERT", "UPDATE", "DELETE")):
            print("🧠 Converting Natural Language to SQL via IDE Bridge...")
            sql = self._text_to_sql(nl_text)
            if not sql:
                return {"status": "ERROR", "msg": "NL-to-SQL conversion via IDE Bridge failed."}

        # Выполнение SQL
        print(f"⚡ Executing SQL: {sql}")
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql)
            
            if sql.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                data = [dict(row) for row in rows]
                conn.close()
                return {"status": "SUCCESS", "data": data, "count": len(data)}
            else:
                conn.commit()
                conn.close()
                return {"status": "SUCCESS", "msg": "Operation completed."}
                
        except Exception as e:
            return {"status": "ERROR", "msg": f"SQL Error: {str(e)}"}

    def _text_to_sql(self, text):
        """
        Requesting SQL generation from the IDE Agent (Gemini).
        """
        try:
            from ide_bridge import IDEBridge
            bridge = IDEBridge()
            
            schema = self._get_schema()
            
            payload = {
                "request": text,
                "schema": schema,
                "instruction": "Convert the natural language request into a valid SQLite query. Return ONLY raw SQL."
            }
            
            sql = bridge.request_llm("TEXT_TO_SQL", payload)
            if sql and "```sql" in sql:
                sql = sql.split("```sql")[1].split("```")[0].strip()
            return sql
        except:
            return None

    def _get_schema(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        schema = "\n".join([f"Table: {r[0]}\nSchema: {r[1]}" for r in cursor.fetchall()])
        conn.close()
        return schema

if __name__ == "__main__":
    agent = DBChatAgent()
    query_text = sys.argv[1] if len(sys.argv) > 1 else "SELECT name FROM sqlite_master"
    res = agent.query(query_text)
    print(json.dumps(res, indent=4, ensure_ascii=False))
