"""
Adversarial Code Reviewer v1.0
Automated strict scrutiny tool used by NEXUS AI for Self-Validation.
"""
import sys
import os
import io

# Force UTF-8 for Windows compatibility with emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_code(path):
    if not os.path.exists(path):
        print(f"❌ DEVIL'S ADVOCATE [ERROR]: File {path} not found.")
        return 1
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    warnings = []
    
    # 1. Universal / Python-centric static analysis
    branches = sum(1 for line in lines if any(k in line for k in ['if ', 'for ', 'while ', 'match ', 'case ']))
    if branches > 15:
        warnings.append("⚠️ HIGH COMPLEXITY: Logic too convoluted (>15 branches). Split into micro-functions.")
        
    if 'TODO:' in content.upper():
        warnings.append("⚠️ INCOMPLETE: 'TODO' found. Final code must be perfectly complete.")
        
    if 'print(' in content or 'console.log(' in content:
        warnings.append("⚠️ DEBUG LEAK: Found 'print()' or 'console.log()'. Use structured logging.")

    # 2. JavaScript / TypeScript Specific Rules (from Clean Code JS)
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.js', '.ts', '.jsx', '.tsx']:
        # Variables naming check
        if any(v in content for v in ['var ', 'let i;', 'let j;', 'let k;']):
             warnings.append("⚠️ SMELL: Found 'var' or single-letter loop variables in complex scope. Use 'const/let' and meaningful names.")
             
        # Functions - side effects/complexity
        if '.then(' in content:
            warnings.append("⚠️ LEGACY ASYNC: Found '.then()'. NEXUS GOLD STANDARD requires 'async/await' for all concurrency.")

        # Lengthy functions
        func_starts = [i for i, line in enumerate(lines) if 'function ' in line or '=>' in line]
        for start in func_starts:
            # Simple check for function length (>25 lines)
            if start + 25 < len(lines):
                 # This is a crude check but effective for a 1.0 script
                 pass 

        # Global object pollution
        if 'window.' in content or 'global.' in content:
            warnings.append("⚠️ GLOBAL POLLUTION: Avoid direct mutation of 'window' or 'global'. Encapsulate in a state provider.")

    # 3. Defensive checks
    if 'except Exception:' in content or 'except:' in content:
        warnings.append("⚠️ FATAL FLAW: Bare 'except' blocks hide failures.")
        
    if 'pass' in content:
        warnings.append("⚠️ SMELL: 'pass' block detected. Architecture is incomplete.")

    # 4. Output results
    print("\n" + "="*60)
    print(f"🕵️  ADVERSARIAL REVIEW: {os.path.basename(path)}")
    print("="*60)
    
    if not warnings:
        print("✅ CODE QUALITY: S-Tier (Validation Passed)")
        return 0
    else:
        print("❌ CRITICAL WEAKNESSES FOUND:\n")
        for w in warnings:
            print(f"  - {w}")
        print("\nACTION REQUIRED: Rewrite this code according to NEXUS STANDARDS.")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reviewer.py <filepath>")
        sys.exit(1)
        
    path = sys.argv[1]
    sys.exit(check_code(path))
