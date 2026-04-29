import re

with open('tmp_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure we don't accidentally match anything else. The `<pre>` starts at `<pre>` and ends at `</pre>`.
OLD_ARCH_MATCH = re.search(r'<pre>.*?</pre>', html, re.DOTALL)
if OLD_ARCH_MATCH:
    OLD_ARCH = OLD_ARCH_MATCH.group(0)
    
    NEW_ARCH = """<pre>                                  +---------------------------------+
                                  |         CONSTITUTION.md         |
                                  |  (Hot Memory / Arch. Laws)      |
                                  +---------------+-----------------+
                                                  |
                                                  v
                                  +---------------------------------+
                                  |       NEXUS Orchestrator        |
                                  | (Dispatcher + LangGraph/CrewAI) |
                                  +---------------+-----------------+
                                                  |
                 +--------------------------------+--------------------------------+
                 |                                |                                |
                 v                                v                                v
     +-----------------------+        +-----------------------+        +-----------------------+
     |       Frontend        |        |        Backend        |        |       AI Agents       |
     |   Astro v5, Next 15   |        | FastAPI / Python 3.13 |        | 25 Specialized Skills |
     | GSAP/Three.js/Svelte  |        |  Hono, Celery+Redis   |        |   Claude 3.5 / 3.7    |
     +-----------------------+        +-----------------------+        +-----------------------+

     [==============================> 6-LEVEL MEMORY SYSTEM &lt;==============================]
     +-------+  +--------+  +-------------+  +--------------+  +-----------+  +----------+
     |  HOT  |  |  COLD  |  |    STATE    |  |    FAULT     |  | DATABASE  |  |  GRAPH   |
     | Const |  |Doc/Spec|  | memory.json |  |fault_registry|  |SQLite core|  |Neo4j/MCP |
     +-------+  +--------+  +-------------+  +--------------+  +-----------+  +----------+

     [========================> MCP NEURAL NET - 22 CONNECTORS &lt;========================]
     +---------+ +----------+ +----------+ +-----------+ +----------+ +------------------+
     | filesys | |git/github| |bravesrch | | puppeteer | | supabase | |  sentry/neo4j    |
     +---------+ +----------+ +----------+ +-----------+ +----------+ +------------------+

     [=======================> SPECIALIZED SKILLS &amp; PIPELINES &lt;=========================]
     +--------------------+ +--------------------+ +------------------+ +----------------+
     |  OSINT Tactician   | |   Security Audit   | | Document Factory | | Motion Design  |
     | domain-intel+crawl | | OWASP + AI Defense | | PDF/DOCX Engines | |  GSAP / Video  |
     +--------------------+ +--------------------+ +------------------+ +----------------+

     [======================> 26 AUTONOMOUS SLASH-COMMANDS &lt;============================]
     &gt; /status  &gt; /deploy  &gt; /turbo  &gt; /motion  &gt; /pdf  &gt; /audit  &gt; /github  &gt; [19 more]

     [=============================> MONETIZATION VECTORS &lt;=============================]
     +--------------------------+ +---------------------------+ +------------------------+
     |        BUG BOUNTY        | |     DATA MINING B2B       | |   FREELANCE FACTORY    |
     | OSINT / HackerOne / BWC  | |  Firecrawl + CSV Leads    | | JustDoIt + AutoDeploy  |
     +--------------------------+ +---------------------------+ +------------------------+</pre>"""
    
    html = html.replace(OLD_ARCH, NEW_ARCH)
    with open('tmp_presentation.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected new massive ASCII architecture.")
else:
    print("Could not find <pre> block.")
