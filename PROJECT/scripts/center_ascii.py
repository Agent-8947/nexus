import re

lines = [
    "+-----------------------------+",
    "|       CONSTITUTION.md       |",
    "|  (Hot Memory / Arch. Laws)  |",
    "+-------------+---------------+",
    "|",
    "v",
    "+-----------------------------+",
    "|      NEXUS Orchestrator     |",
    "| (Dispatcher+LangGraph/Crew) |",
    "+-------------+---------------+",
    "|",
    "+-------------------------+-------------------------+",
    "|                         |                         |",
    "v                         v                         v",
    "+-------------------+  +-------------------+  +-------------------+",
    "|     Frontend      |  |      Backend      |  |     AI Agents     |",
    "| Astro v5/Next 15  |  |FastAPI/Python 3.13|  |25 Specialized Skll|",
    "|GSAP/Three / Svelte|  |Hono / Celery+Redis|  | Claude 3.5 / 3.7  |",
    "+-------------------+  +-------------------+  +-------------------+",
    "",
    "[=================> 6-LEVEL MEMORY SYSTEM <=================]",
    "+-----+ +----+ +---------+ +------------+ +-------+ +-------+",
    "| HOT | |COLD| |  STATE  | |   FAULT    | |  DB   | | GRAPH |",
    "|Const| |Docs| |memre/fst| |fault_regist| |SQLite | | Neo4j |",
    "+-----+ +----+ +---------+ +------------+ +-------+ +-------+",
    "",
    "[===============> MCP NEURAL NET - 22 CONNECTORS <==============]",
    "+-------+ +-------+ +-------+ +---------+ +--------+ +----------+",
    "|filesys| |git/github| |brave| |puppeteer| |supabase| |sentry/neo|",
    "+-------+ +-------+ +-------+ +---------+ +--------+ +----------+",
    "",
    "[==============> SPECIALIZED SKILLS & PIPELINES <===============]",
    "+----------------+ +----------------+ +------------+ +----------+",
    "|OSINT Tactician | | Security Audit | |Doc. Factory| |Motion Des|",
    "|domain+firecrawl| |OWASP+AI Defense| |PDF/DOCX gen| |GSAP/Video|",
    "+----------------+ +----------------+ +------------+ +----------+",
    "",
    "[==============> 26 AUTONOMOUS SLASH-COMMANDS <=================]",
    "> /status   > /deploy   > /turbo   > /motion   > /pdf   > /audit",
    "",
    "[====================> MONETIZATION VECTORS <===================]",
    "+-----------------------+ +------------------+ +----------------+",
    "|      BUG BOUNTY       | | DATA MINING B2B  | | FREELANCE FACT |",
    "|OSINT/HackerOne/Bugcrwd| | Firecrawl+CSV LL | | Justdoit+Auto  |",
    "+-----------------------+ +------------------+ +----------------+"
]

max_len = max(len(l) for l in lines)

centered_lines = []
for l in lines:
    centered = l.center(max_len)
    escaped = centered.replace('<', '&lt;').replace('>', '&gt;')
    centered_lines.append(escaped)

new_pre = '<pre style="margin: 0 auto; width: max-content;">' + '\n'.join(centered_lines) + '</pre>'

with open('tmp_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

OLD_ARCH_MATCH = re.search(r'<pre>.*?</pre>', html, re.DOTALL)
if OLD_ARCH_MATCH:
    OLD_ARCH = OLD_ARCH_MATCH.group(0)
    
    # If the <pre> had style attr before it would be overwritten, but we regex searched for <pre> (without attributes)
    # Let's search with optionally attributes
    OLD_ARCH_MATCH_FLEX = re.search(r'<pre[^>]*>.*?</pre>', html, re.DOTALL)
    if OLD_ARCH_MATCH_FLEX:
        OLD_ARCH = OLD_ARCH_MATCH_FLEX.group(0)

    html = html.replace(OLD_ARCH, new_pre)
    with open('tmp_presentation.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected strictly centered ASCII architecture.")
else:
    print("Could not find <pre> block.")
