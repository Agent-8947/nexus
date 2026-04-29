# NEXUS Synthesis Protocol v6.0
## For ANY model (Flash/Haiku/3B) — follow mechanically

### STEP 1: User says "проведи синтез" or "synthesize"
Run this command EXACTLY:
```
python DNA_09_Mission_Control.py --mission security --seed <random_4_digits>
```

### STEP 2: Verify output
Check the output for:
- `DOMAIN_COMPOSED(X+Y)` — means Domain Blocks worked ✅
- `SCAFFOLD_ONLY` — means fallback, check DNA_23_Domain_Blocks.py exists

### STEP 3: Validate generated agents
```
python -c "import ast; from pathlib import Path; [print(f'  OK  {f.name}') for f in Path('DNA_12_AST_RENDER').glob('HYBRID_*_synthesized_agent.py') if ast.parse(f.read_text(encoding='utf-8'))]"
```

### STEP 4: Report to user
Show:
- Number of agents synthesized
- Accepted/Rejected counts
- Current DNA Core node count
- Domain combinations used

### KEY: You do NOT write agent code yourself.
The assembler (DNA_10_Code_Assembler.py) uses DNA_23_Domain_Blocks.py
to compose unique agents from pre-written blocks. Your role is to:
1. Run the command
2. Monitor output
3. Report results

### Available missions: security, osint, ai, infra, web, data
### Available seeds: any 4-digit number
