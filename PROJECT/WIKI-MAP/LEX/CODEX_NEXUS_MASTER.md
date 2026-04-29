# 🏛️ CODEX NEXUS: ACTIVE LAWS MASTER FILE
**Status**: EXECUTABLE CONTRACTS ONLY
**Compiled by**: AGENT 18 (LEGISLATOR) [NO STUBS]

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

---

# LEX-NEXUS 02: THE LAW OF STEALTH RECONNAISSANCE
**Status**: ENFORCED
**Applies to**: ALL NETWORK-BOUND AGENTS

### 1. CAPTCHA ABSTINENCE
No agent is allowed to perform direct `urllib` requests against High-Protection domains (Google Search, LinkedIn, Glassdoor) without rotation.

### 2. THE PROXY PATTERN (AGNOSTIC SCOUT)
Agents must use DuckDuckGo HTML or SearX as a buffer layer to extract snippets before attempting direct domain contact.

### 3. BROWSER EMULATION (HEADLESS TASK)
If direct data extraction is required, the agent must spawn a Playwright browser context with:
- `headless: true`
- Randomized `User-Agent` (Chrome 130+)
- Spoofed `Referer` (Google / Bing)

### 4. SUCCESS METRIC
An agent module must return at least 1 lead per run. Failure to yield results triggers an automatic logic swap (Retry Loop).