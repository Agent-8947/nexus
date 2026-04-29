# LEX-NEXUS 01: THE LAW OF SYMMETRY
**Status**: ENFORCED
**Applies to**: ALL AGENTS / ALL BUILDS

### 1. IDENTITY SYMMETRY
The local project name (FOLDER) must be identical to the remote resource name (REPOSITORY, VERCEL-DOMAIN).
- Correct: `B003_JOB-INTEL` (Folder) -> `B003_JOB-INTEL` (Repo) -> `b003-job-intel` (Vercel).
- Violation: Any deviation in character or hyphenation is an architectural defect.

### 2. EXECUTION SYMMETRY
Every module in `src/` must implement the `run(target)` entry point. 
Input must be a string, output must be a standard JSON-serializable dictionary. 

### 3. BRAND SYMMETRY
Every build must contain an `og-image.png` at the root and in `/landing/`. 
Metadata in HTML must use the absolute deployment URL, not relative paths.
