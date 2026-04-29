---
name: blockchain-auditor
description: Smart contract safety scanner and zk-proof verifier.
---

## USE FOR
- Static analysis of Solidity/Rust smart contracts to identify reentrancy and integer overflow vulnerabilities.
- Validating the mathematical proofs of zk-SNARK integrations within NEXUS sub-systems.
- Auditing transaction costs (gas) across heavily utilized on-chain paths.

## Instructions
1. **Audit Constraint:** Evaluate AST and opcodes using standard frameworks. Avoid heuristic guessing of contract logic.
2. **Vulnerability Prioritization:** Any flash-loan exploit vector or uninitialized proxy state must issue an immediate CI blocking signal.
3. **Execution Protocol:**
   - [Decompile] Pull Bytecode and reverse if source is unavailable.
   - [Symbolic Execution] Trace execution paths for locked funds.
   - [Verdict] Output JSON strictly detailing line numbers of critical defects.
4. **Zero-Hallucination Policy:** Never output "looks safe" without a complete mathematical trace. If complexity exceeds bounds, abort and flag for human review.
