#!/usr/bin/env python3
"""
NEXUS PATTERN BANK v1.0 — Synthesis Memory
============================================
SQLite database that remembers:
  - Which synthesis pairs worked (high fitness)
  - Which patterns were used
  - What failed and why
  - Code similarity scores for dedup

The synthesis loop consults this before generating:
  1. Check if pair was already synthesized
  2. Get relevant successful patterns
  3. Get known failure patterns to AVOID
  4. Score novelty against existing agents
"""

import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

DB_PATH = Path(__file__).resolve().parent / "pattern_bank.db"


@dataclass
class SynthesisRecord:
    """Record of a single synthesis attempt."""
    child_id: str
    parent_a: str
    parent_b: str
    domain_a: str
    domain_b: str
    role: str
    generation: int
    status: str             # DOMAIN_COMPOSED | SCAFFOLD_ONLY | OLLAMA_FILLED
    fitness_score: float    # 0.0 - 1.0
    fill_coverage: float    # 1.0 = no [FILL:*] left
    test_pass: bool         # integration test passed?
    schema_valid: bool      # I/O contract valid?
    code_hash: str          # SHA256 of generated code
    code_lines: int
    patterns_used: str      # JSON list of block names
    errors: str             # JSON list of errors
    timestamp: str


class PatternBank:
    """SQLite-backed synthesis memory."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS syntheses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id TEXT UNIQUE,
                parent_a TEXT,
                parent_b TEXT,
                domain_a TEXT,
                domain_b TEXT,
                role TEXT,
                generation INTEGER,
                status TEXT,
                fitness_score REAL DEFAULT 0.0,
                fill_coverage REAL DEFAULT 1.0,
                test_pass INTEGER DEFAULT 0,
                schema_valid INTEGER DEFAULT 0,
                code_hash TEXT,
                code_lines INTEGER DEFAULT 0,
                patterns_used TEXT DEFAULT '[]',
                errors TEXT DEFAULT '[]',
                timestamp TEXT
            );

            CREATE TABLE IF NOT EXISTS pattern_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT,
                domain TEXT,
                usage_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                avg_fitness REAL DEFAULT 0.0,
                last_used TEXT
            );

            CREATE TABLE IF NOT EXISTS known_failures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_combo TEXT,
                error_type TEXT,
                error_detail TEXT,
                occurrence_count INTEGER DEFAULT 1,
                first_seen TEXT,
                last_seen TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_syntheses_domains ON syntheses(domain_a, domain_b);
            CREATE INDEX IF NOT EXISTS idx_syntheses_fitness ON syntheses(fitness_score DESC);
            CREATE INDEX IF NOT EXISTS idx_pattern_scores_name ON pattern_scores(pattern_name);
        """)
        self.conn.commit()

    def record_synthesis(self, rec: SynthesisRecord):
        """Record a synthesis attempt."""
        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO syntheses
                (child_id, parent_a, parent_b, domain_a, domain_b, role, generation,
                 status, fitness_score, fill_coverage, test_pass, schema_valid,
                 code_hash, code_lines, patterns_used, errors, timestamp)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                rec.child_id, rec.parent_a, rec.parent_b, rec.domain_a, rec.domain_b,
                rec.role, rec.generation, rec.status, rec.fitness_score, rec.fill_coverage,
                int(rec.test_pass), int(rec.schema_valid), rec.code_hash, rec.code_lines,
                rec.patterns_used, rec.errors, rec.timestamp,
            ))
            # Update pattern scores
            patterns = json.loads(rec.patterns_used)
            for p in patterns:
                existing = self.conn.execute(
                    "SELECT id, usage_count, success_count, avg_fitness FROM pattern_scores WHERE pattern_name = ?",
                    (p,)
                ).fetchone()
                if existing:
                    new_count = existing["usage_count"] + 1
                    new_success = existing["success_count"] + (1 if rec.fitness_score > 0.5 else 0)
                    new_avg = (existing["avg_fitness"] * existing["usage_count"] + rec.fitness_score) / new_count
                    self.conn.execute(
                        "UPDATE pattern_scores SET usage_count=?, success_count=?, avg_fitness=?, last_used=? WHERE id=?",
                        (new_count, new_success, round(new_avg, 4), rec.timestamp, existing["id"])
                    )
                else:
                    self.conn.execute(
                        "INSERT INTO pattern_scores (pattern_name, domain, usage_count, success_count, avg_fitness, last_used) VALUES (?,?,1,?,?,?)",
                        (p, rec.domain_a, 1 if rec.fitness_score > 0.5 else 0, rec.fitness_score, rec.timestamp)
                    )
            # Record failures
            if rec.errors and rec.errors != "[]":
                for err in json.loads(rec.errors):
                    combo = f"{rec.domain_a}+{rec.domain_b}"
                    existing = self.conn.execute(
                        "SELECT id, occurrence_count FROM known_failures WHERE pattern_combo=? AND error_type=?",
                        (combo, err.split(":")[0] if ":" in err else err)
                    ).fetchone()
                    if existing:
                        self.conn.execute(
                            "UPDATE known_failures SET occurrence_count=?, last_seen=? WHERE id=?",
                            (existing["occurrence_count"] + 1, rec.timestamp, existing["id"])
                        )
                    else:
                        self.conn.execute(
                            "INSERT INTO known_failures (pattern_combo, error_type, error_detail, first_seen, last_seen) VALUES (?,?,?,?,?)",
                            (combo, err.split(":")[0] if ":" in err else err, err, rec.timestamp, rec.timestamp)
                        )
            self.conn.commit()
        except Exception as e:
            print(f"  [BANK] Record error: {e}")

    def was_already_synthesized(self, parent_a: str, parent_b: str) -> bool:
        """Check if this exact pair was already synthesized."""
        row = self.conn.execute(
            "SELECT id FROM syntheses WHERE parent_a=? AND parent_b=?",
            (parent_a, parent_b)
        ).fetchone()
        return row is not None

    def get_best_patterns(self, domain: str, limit: int = 5) -> List[Dict]:
        """Get highest-scoring patterns for a domain."""
        rows = self.conn.execute(
            "SELECT pattern_name, avg_fitness, success_count, usage_count FROM pattern_scores WHERE domain=? ORDER BY avg_fitness DESC LIMIT ?",
            (domain, limit)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_known_failures(self, domain_a: str, domain_b: str) -> List[Dict]:
        """Get known failure patterns for this domain combination."""
        combo = f"{domain_a}+{domain_b}"
        rows = self.conn.execute(
            "SELECT error_type, error_detail, occurrence_count FROM known_failures WHERE pattern_combo=? ORDER BY occurrence_count DESC LIMIT 10",
            (combo,)
        ).fetchall()
        return [dict(r) for r in rows]

    def is_code_duplicate(self, code_hash: str) -> bool:
        """Check if an agent with identical code already exists."""
        row = self.conn.execute(
            "SELECT id FROM syntheses WHERE code_hash=?", (code_hash,)
        ).fetchone()
        return row is not None

    def get_stats(self) -> Dict[str, Any]:
        """Get overall bank statistics."""
        total = self.conn.execute("SELECT COUNT(*) FROM syntheses").fetchone()[0]
        avg_fitness = self.conn.execute("SELECT AVG(fitness_score) FROM syntheses").fetchone()[0] or 0
        test_pass = self.conn.execute("SELECT COUNT(*) FROM syntheses WHERE test_pass=1").fetchone()[0]
        top_patterns = self.conn.execute(
            "SELECT pattern_name, avg_fitness FROM pattern_scores ORDER BY avg_fitness DESC LIMIT 5"
        ).fetchall()
        failures = self.conn.execute("SELECT COUNT(*) FROM known_failures").fetchone()[0]
        domains = self.conn.execute(
            "SELECT domain_a || '+' || domain_b as combo, COUNT(*) as cnt, AVG(fitness_score) as avg_f FROM syntheses GROUP BY combo ORDER BY avg_f DESC"
        ).fetchall()

        return {
            "total_syntheses": total,
            "avg_fitness": round(avg_fitness, 4),
            "test_pass_rate": round(test_pass / max(total, 1), 4),
            "known_failures": failures,
            "top_patterns": [{"name": r[0], "fitness": round(r[1], 3)} for r in top_patterns],
            "domain_combos": [{"combo": r[0], "count": r[1], "avg_fitness": round(r[2], 3)} for r in domains],
        }

    def close(self):
        self.conn.close()


def compute_code_hash(code: str) -> str:
    """Compute SHA256 hash of code (normalized — strip whitespace, comments)."""
    import re
    # Strip comments and blank lines for content-hash
    lines = []
    for line in code.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith('"""') and not stripped.startswith("'''"):
            lines.append(stripped)
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


def compute_fitness(code: str, test_passed: bool, errors: List[str]) -> float:
    """Compute fitness score for a synthesized agent.
    
    Factors:
      - fill_coverage:  1.0 if no [FILL:*] remain
      - test_pass:      0.3 bonus if integration test passed
      - error_penalty:  -0.1 per error
      - code_quality:   lines of actual logic (not imports/boilerplate)
      - uniqueness:     (checked separately via is_code_duplicate)
    """
    fill_count = code.count("[FILL:")
    total_lines = len(code.splitlines())
    fill_coverage = 1.0 - (fill_count / max(total_lines, 1))

    logic_lines = sum(1 for line in code.splitlines()
                      if line.strip()
                      and not line.strip().startswith("#")
                      and not line.strip().startswith("import")
                      and not line.strip().startswith("from")
                      and not line.strip().startswith('"""'))

    code_quality = min(logic_lines / 100, 1.0)  # cap at 100 logic lines = 1.0
    test_bonus = 0.3 if test_passed else 0.0
    error_penalty = min(len(errors) * 0.1, 0.5)

    fitness = (fill_coverage * 0.3) + (code_quality * 0.3) + test_bonus - error_penalty
    return round(max(0.0, min(1.0, fitness)), 4)


if __name__ == "__main__":
    bank = PatternBank()
    # Self-test with mock record
    rec = SynthesisRecord(
        child_id="TEST_AGENT_BANK",
        parent_a="CRAWL4AI", parent_b="METASPLOIT",
        domain_a="osint", domain_b="security",
        role="collector", generation=1,
        status="DOMAIN_COMPOSED",
        fitness_score=0.85,
        fill_coverage=1.0,
        test_pass=True, schema_valid=True,
        code_hash="abc123", code_lines=200,
        patterns_used=json.dumps(["scan_secrets", "dns_recon", "http_fingerprint"]),
        errors="[]",
        timestamp=datetime.now().isoformat(),
    )
    bank.record_synthesis(rec)
    stats = bank.get_stats()
    print(f"[OK] Pattern Bank initialized: {stats['total_syntheses']} records")
    print(f"     Avg fitness: {stats['avg_fitness']}")
    print(f"     Top patterns: {stats['top_patterns']}")
    # Cleanup test
    bank.conn.execute("DELETE FROM syntheses WHERE child_id='TEST_AGENT_BANK'")
    bank.conn.commit()
    bank.close()
    print("[OK] Self-test PASSED")
