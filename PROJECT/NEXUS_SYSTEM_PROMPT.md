# 🤖 SYSTEM PROMPT / CONTEXT SNAPSHOT: NEXUS OS

**Instruction for LLM**: Read the following context carefully to understand the structure, architecture, and current state of the NEXUS project. Proceed with the user's task ONLY after assimilating this information.

---

## 1. PROJECT IDENTITY

- **Name**: NEXUS OS (Cognitive Operating System for IDEs)
- **Archetype**: `AI-Orchestrated-NEXUS-v2`
- **Philosophy**: *"Codified Context"* (Every action, error, and decision is archived in real-time memory).
- **Goal**: Transform a standard local IDE into an autonomous command center capable of self-healing, multi-agent orchestration, generating professional documents, and controlling physical hardware/mobile devices.

## 2. MULTI-LAYER MEMORY SYSTEM

NEXUS uses an advanced persistent memory loop:

1. **Hot Memory** (`CONSTITUTION.md`): Strict architectural laws. Must be read at the start of every session.
2. **Cold Memory** (`DOCS/SPECS/*.md`): Architectural maps and feature specifications.
3. **State Memory** (`memory.json`): Current active stack, history logs, and system protocols.
4. **Fault Memory** (`fault_registry.json`): Registry of all past errors to prevent recurrence (Self-Healing).
5. **Database Memory** (`nexus_optimus.db`): SQLite database tracking all executed commands and API metrics.
6. **Graph Context** (MCP Memory Server): Dynamic relations between project entities.

## 3. CORE ARCHITECTURE & PERFORMANCE

- **Throughput**: Verified at **104,000 msg/s** using Python Named Pipes protocol.
- **Backend v2.0**: Unified FastAPI server (`main.py`) running the Dispatcher, APIs, and SQLite command logs. All endpoints validated at Exit Code 0.
- **MCP Neural Net**: Connected to **20+ external interfaces** (filesystem, git, sqlite, brave-search, sentry, puppeteer, and **PARE Optimized Tools**), allowing the AI to "see" and "do" everything a developer can.
- **Pare Integration**: Uses structured, token-efficient MCP servers for CLI tools.

## 4. CURRENT TECHNOLOGY STACK

- **Frontend**: Astro v5, Next.js 15, Svelte (Islands), Tailwind CSS, GSAP 3.12 (Motion).
- **Backend**: FastAPI (Python 3.13), Hono (TS Edge API), Celery + Redis.
- **AI Automation**: Vercel AI SDK, LangGraph, CrewAI, Crawl4AI. Model: Anthropic Claude 3.5/3.7.
- **Database**: Supabase (PostgreSQL), Cloudflare D1, Upstash Redis.
- **DevOps**: Vercel/Cloudflare (deploy), GitHub Actions, Docker.
- **Hardware/Physical**: 3D Forge (`build123d`/OpenSCAD), PhoneDriver (Mobile ADB Automation via `NexusVLAgent`).

## 5. FLEET OF AI AGENTS (Skills & Roles)

The system routes tasks to specialized sub-agents:

- `Dispatcher`: The supervisor routing tasks to appropriate nodes.
- `Self-Healing Agent`: Detects crashes/lints and auto-patches the codebase.
- `Document Factory`: Creates professional Business/Marketing PDFs and websites with self-critique loops.
- `Phone Driver (nexus-mobile-driver)`: Vision-based (VL) mobile GUI automation over ADB.
- `Marketing Strategist`: Generates comprehensive marketing strategies.
- `DB Chat Agent (NL2SQL)`: Queries databases using natural language.

## 6. SLASH COMMAND WORKFLOWS (Supported Tools)

NEXUS exposes functionality via modular slash commands.
*Examples:* `/status`, `/turbo`, `/deploy`, `/pdf`, `/vercel`, `/github`, `/test`, `/audit`, `/idea`, `/motion`, `/clean-code`, `/token`, `/prime`, `/+` (report error).

## 7. RECENT MILESTONES

- Refactored presentation website with multi-language support (EN, UA, RU) and dynamic PDF generation.
- Integrated `PhoneDriver` as a built-in skill utilizing the IDE's native vision models (`NexusVLAgent`).
- Successfully deployed presentation site to Vercel (`nexus-presentation-v2.vercel.app`) with GitHub sync.

## 8. DIRECTIVES FOR YOU (THE LLM)

1. **Never guess**. If a request is vague, trigger the "Ambiguity Gate" and ask for clarification.
2. **Execute, don't simulate**. Whenever possible, write code that works out-of-the-box and uses absolute paths within `PROJECT/`.
3. **Respect the Constitution**. Maintain "Agnostic Excellence" and "Stack Purity". Avoid legacy packages.
4. **Prefer Pare MCP Tools**. Always use Pare MCP tools (`pare-git`, `pare-github`, `pare-search`, etc.) instead of raw CLI commands in the shell. Pare provides structured JSON and reduces token consumption by 40-70%.

---

### STATUS: READY TO ASSIST
