# AGNOSTIC ARCHITECTURE DECISION RECORD (ADR) - NEXUS v2.1

## 1. Context & Objectives

Мы проводим независимый архитектурный аудит системы **IDE-optimus (NEXUS)**.
**Цель**: Масштабируемая оркестрация ИИ с гарантированной производительностью 100k msg/s на "Lite" железе (ноутбук, 6GB RAM) при сохранении возможности Edge-деплоя.

---

## 2. Technology Matrix Selection

Сравнение 3-х альтернативных путей исполнения, игнорируя текущую привязку к Python/Go.

| Критерий | **Option A: Rust-Obsessed** | **Option B: Node-Enterprise** | **Option C: Go-Native** |
| :--- | :--- | :--- | :--- |
| **Backend Core** | Rust (Axum / Tokio) | Node.js (NestJS / Fastify) | Go (Fiber / StdLib) |
| **API Bridge** | WebSockets (Tungstenite) | gRPC / Socket.io | FastHTTP / gRPC |
| **Frontend** | Solid.js (Leightweight) | Next.js (Fullstack) | HTMX + Go Templates |
| **DB Layer** | SurrealDB (Embedded) | PostgreSQL (Prisma) | BadgerDB / SQLite |
| **Development Speed** | 4/10 (Slow, strict) | **9/10 (Highest)** | 7/10 (Moderate) |
| **Runtime Performance**| **10/10 (Maximum)** | 6/10 (GC overhead) | 9/10 (Predictable) |
| **Memory Footprint** | **~50 MB (Uktra-low)** | ~500 MB (High) | ~150 MB (Low) |

---

## 3. Trade-offs Analysis (The Matrix)

### **Alpha: Rust (Axum + Tauri)**

* **PROS**: Нулевой оверхед (Zero-cost abstractions), полное отсутствие Garbage Collector (GC), максимальная безопасность памяти. Лучший выбор для 100k msg/s.
* **CONS**: Самый высокий порог входа. Сложность написания AI-агентов (отсутствие зрелых библиотек а-ля LangChain/Pydantic).
* **Score**: Performance: 10, DX: 3.

### **Beta: Node.js (NestJS + Fastify)**

* **PROS**: Огромная экосистема, TypeScript везде, отличные AI SDK от Vercel. Быстрая разработка.
* **CONS**: Пожирание RAM (особенно NestJS). Задержки из-за GC при пиковой нагрузке 100k msg/s.
* **Score**: Performance: 6, DX: 10.

### **Gamma: Go (Fiber + Fiber)**

* **PROS**: Простая многопоточность (Goroutines), один бинарник на выходе, отличная производительность.
* **CONS**: Меньше библиотек для глубокой работы с Docx/PDF и сложной AI-логики по сравнению с Python.
* **Score**: Performance: 9, DX: 7.

---

## 4. Final Architecture Decision: THE HYBRID NEXUS (Validated)

После анализа мы принимаем **Гибридный NEXUS v2.1 (Python + Hono + Astro)** как наиболее сбалансированное решение.

**Почему не чистый Rust?** Скорость разработки AI-функций на Python в 10 раз выше, а Named Pipes (IPC) нивелирует разницу в производительности сетевого стека.

**Почему не NestJS?** Мы не можем позволить себе тратить 500MB RAM на простой сервер при 6GB общего объема.

### **Final Selection Summary:**

- **Logic Core**: Python 3.13 (для AI и документов).
* **Communication**: Windows Named Pipes (для 100k+ msg/s).
* **Edge Frontend**: Astro v5 + Hono (для Edge-скорости).
* **Local Storage**: SQLite (Zero-latency).

---

## 5. Hardware Requirement Specification

### **Minimum (Low-load / Dev)**

* **CPU**: 4 Cores (2.0 GHz)
* **RAM**: 4 GB (2GB OS + 1GB Python + 1GB Browser)
* **OS**: Windows 10/11 (для Named Pipes) или Ubuntu 22.04 (для Unix Sockets)

### **Recommended (Target 100k msg/s)**

* **CPU**: 8+ Cores (Apple M1/M2/M3 or Ryzen 7+)
* **RAM**: 8-16 GB (для комфортной работы с AI-агентами в памяти)
* **Storage**: NVMe SSD (критично для SQLite при записи логов)

### **System Configuration (Turbo-Boost)**

* **File Descriptors**: 10,000+
* **Memory Pages**: Enable Large Pages if possible.
* **Network**: Loopback optimization in Windows Defender.

---

## 6. Consequences

* **Wins**: Максимально быстрый вывод фич (Time-to-Market), отличный UI, запредельная локальная скорость.
* **Sacrifices**: Мы жертвуем "чистотой одного языка" (потребуются Python и TypeScript).

---
**© Agnostic Architecture Engine | NEXUS v2.1 | Approved: 2026-02-28**
