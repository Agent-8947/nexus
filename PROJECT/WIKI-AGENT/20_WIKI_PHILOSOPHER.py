#!/usr/bin/env python3
"""
NEXUS AGENT 20 - WIKI PHILOSOPHER [LAW MINER]
-------------------------------------------
Mission: Autonomous extraction of architectural invariants from 1400+ Wiki Repositories.
Synthesize raw engineering concepts into executable LEX laws.
"""

import os
import json
import random
import time
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения (.env) для работы API-ключа
load_dotenv(os.path.join(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT", ".env"))

SYSTEM_PROMPT = """
Ты — WIKI PHILOSOPHER (АГЕНТ 20). 
Твоя задача — анализировать архитектуру и функционал лучших мировых репозиториев из Библиотеки NEXUS. 
Основываясь на паттернах этих проектов, выведи АБСОЛЮТНЫЙ АРХИТЕКТУРНЫЙ ЗАКОН, который должен соблюдаться всеми автономными агентами при генерации кода или систем.

Напиши ровно 1 закон. Никаких извинений, приветствий или рассуждений вне шаблона. Формат STRICT MARKDOWN.

ШАБЛОН ОТВЕТА:
# LEX-NEXUS {ID_PLACEHOLDER}: LAW OF [СУТЬ ЗАКОНА НА АНГЛИЙСКОМ]
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: {DOMAIN}
**Derived from**: [Названия исходных репозиториев/концептов]

### 1. DIRECTIVE
[Строгое, бескомпромиссное правило на русском языке: что агенты обязаны делать или чего обязаны избегать. Без воды. Жесткий технический контракт.]

### 2. SYMMETRY / PATTERN
**VIOLATION (Как делает стандартная LLM):**
[Пример плохого подхода]

**COMPLIANCE (Как требует этот закон):**
[Пример жесткой инженерной логики, архитектуры или сэмпла кода]
"""

class NexusPhilosopher:
    def __init__(self):
        self.wiki_base_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI"
        self.lex_drafts_dir = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-MAP\LEX\DRAFTS"
        
        if not os.path.exists(self.lex_drafts_dir):
            os.makedirs(self.lex_drafts_dir)

    def _call_llm(self, domain, content_samples):
        """ Integrate with Anthropic/OpenAI wrapper """
        
        user_prompt = f"DOMAIN: {domain}\n\nSAMPLES FROM ARCHIVE:\n"
        for i, sample in enumerate(content_samples):
            # Truncating per sample to save context window (getting the meat: ~2000 chars)
            user_prompt += f"--- REPO SAMPLE {i+1} ---\n{sample[:2500]}\n\n"
            
        print("[*] PHILOSOPHER: Thinking... extracting invariants from samples...")
        
        try:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1200,
                temperature=0.4, # Need a bit of creativity to synthesize, but structured
                system=SYSTEM_PROMPT.replace("{DOMAIN}", domain).replace("{ID_PLACEHOLDER}", "[AUTO]"),
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"[-] API call failed ({str(e)[:30]}...). Mocking extraction rule for pipeline demonstration...")
            # Fallback to test pipeline visually
            mock_draft = f"# LEX-NEXUS DRAFT: LAW OF COMPUTATIONAL DENSITY\n**Status**: DRAFT\n**Domain**: {domain}\n**Derived from**: [Sampled repos]\n\n### 1. DIRECTIVE\nЗапрещено использовать циклы 'for' при обработке массивов данных в этом домене. Использовать исключительно векторизованные операции.\n\n### 2. SYMMETRY / PATTERN\n**VIOLATION:**\n```python\nfor item in data:\n    res.append(item*2)\n```\n**COMPLIANCE:**\n```python\nres = data * 2\n```"
            return mock_draft

    def sample_domain(self, target_domain=None, sample_count=4):
        """ Randomly selects a few repositories from the entire Wiki or a specific domain folder to analyze cross-repo patterns. """
        
        all_files = []
        # Fallback to full random if no domain structure is strict, otherwise focus domain
        for root, dirs, files in os.walk(self.wiki_base_path):
            if target_domain and target_domain.lower() not in root.lower():
                continue
            for file in files:
                if file.endswith('.md'):
                    all_files.append(os.path.join(root, file))
                    
        if not all_files:
            print(f"[-] No markdown files found for domain: {target_domain}")
            return []
            
        # Select randomly to find unexpected correlations
        selected = random.sample(all_files, min(sample_count, len(all_files)))
        samples_content = []
        
        for filepath in selected:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                samples_content.append(f"Source: {os.path.basename(filepath)}\n" + f.read())
                
        return samples_content

    def save_draft(self, law_md, domain):
        """ Saves the raw drafted law into the DRAFTS folder for human approval """
        if not law_md: return
        
        timestamp = int(time.time())
        safename = domain if domain else "GENERAL"
        draft_file = os.path.join(self.lex_drafts_dir, f"DRAFT_{safename}_{timestamp}.md")
        
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(law_md)
            
        print(f"[+] INVARIANT EXTRACTED: Draft Law saved to {draft_file}")
        print("[!] ACTION REQUIRED: Review draft and move to /LEX/ to enforce via LEGISLATOR.")

    def mine(self, domain="ROBOTICS"):
        print(f"[*] AGENT 20: Initiating deep extraction on domain '{domain}'...")
        samples = self.sample_domain(domain)
        if not samples: return
        
        law_draft = self._call_llm(domain, samples)
        self.save_draft(law_draft, domain)

if __name__ == "__main__":
    miner = NexusPhilosopher()
    # You can change this to "SECURITY", "ASTRO", "OSINT", "MATH", etc.
    miner.mine("ALGORITHMS")
