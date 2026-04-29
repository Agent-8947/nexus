#!/usr/bin/env python3
import sqlite3
import json
import os

# Registry path
db_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM\NEXUS-FARM-DNA\DNA\nexus_spine_v3.db"

def add_test_task():
    # Payload for Agent 88 (Bayesian Fact Checker)
    payload = {
        "claims": [
            {"text": "Neural signal anomaly detected in TVB repo", "source_rank": 0.95},
            {"text": "Possible GitHub secret leak in WIKI directory", "source_rank": 0.8}
        ]
    }
    
    conn = sqlite3.connect(db_path)
    # Add task for SIGNAL domain (where Agent 88 is registered)
    conn.execute("INSERT INTO task_queue (target_domain, payload) VALUES (?, ?)", 
                 ("SIGNAL", json.dumps(payload)))
    conn.commit()
    conn.close()
    print("✅ TEST TASK ADDED TO NEURAL SPINE")

if __name__ == "__main__":
    add_test_task()
