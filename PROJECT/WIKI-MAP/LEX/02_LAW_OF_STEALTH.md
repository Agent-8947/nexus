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
