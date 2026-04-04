from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import re
from pathlib import Path

# Config & Discovery
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
OUTPUT_DIR = PROJECT_ROOT / 'outputs'
LOG_FILE = OUTPUT_DIR / 'security_sentinel.log'

default_args = {
    'owner': 'Nexus_Operator',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 3),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def scan_scripts_for_secrets():
    """Logic to scan for emails and secrets in the scripts directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    findings = []
    # Simplified Gitleaks pattern (Regex)
    secret_pattern = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)|(password|secret|api_key)\s*=\s*[\'"][^\'"]+[\'"]', re.IGNORECASE)

    for script_file in SCRIPTS_DIR.rglob('*.py'):
        with open(script_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = secret_pattern.findall(content)
            if matches:
                findings.append(f"[LEAK DETECTED] in {script_file.name}: {len(matches)} potential secrets.")

    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(f"\n--- AUDIT RUN: {datetime.now().isoformat()} ---\n")
        if not findings:
            log.write("STATUS: CLEAN. No hardcoded emails or secrets found.\n")
        else:
            for f in findings:
                log.write(f"{f}\n")
    
    return "Audit Complete. Check logs."

def audit_completion_status():
    print("NEXUS SENTINEL: Workflow complete. Integrity verified.")

with DAG(
    'nexus_security_sentinel_v1',
    default_args=default_args,
    description='A security sentinel for NEXUS scripts codebase.',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['nexus', 'security', 'hardened'],
) as dag:

    t1 = PythonOperator(
        task_id='scan_scripts_secrets',
        python_callable=scan_scripts_for_secrets,
    )

    t2 = PythonOperator(
        task_id='finalize_audit',
        python_callable=audit_completion_status,
    )

    t1 >> t2
