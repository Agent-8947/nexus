---
name: motion-principles
description: Systematic rules for meaningful interface animation and kinetic typography. Synthesized from "Designing Interface Animation" (Val Head) and "Design for Motion" (Austin Shaw).
when_to_use: interface animation, kinetic typography, GSAP, motion design, web animation, UX motion, duration, easing, stagger, meaningful motion, UI transitions
allowed-tools: Read Grep
argument-hint: [principle, technique, or easing]
---

# Motion Design Principles (NEXUS Edition)
**Sources**: Val Head, Austin Shaw | **Version**: 2025.05

## 🌊 Core Philosophy: Meaningful Motion
Motion must never be decorative. It should always serve one of three purposes:
1. **Focus**: Direct the user's eye to what's important.
2. **Context**: Explain where an element came from and where it is going.
3. **Feedback**: Confirm a user action or system state.

---

## 📐 Animation Fundamentals

### 1. Timing & Duration
- **Small elements**: 100ms - 200ms.
- **Large transitions**: 300ms - 500ms.
- **Rule**: If it feels slow, it probably is. Respect the user's time.

### 2. Easing (The "Feel")
- **Standard**: `power2.out` (GSAP) — for elements arriving.
- **Entrance**: `back.out(1.7)` — for subtle "pop" effects.
- **Exit**: `power2.in` — for elements leaving quickly.
- **Avoid**: Linear easing (feels robotic and unnatural).

### 3. Stagger (The Rhythm)
- **Rule**: Never animate everything at once.
- **Action**: Use `stagger: 0.1` or `0.05` for lists, cards, or text blocks to create a "wave" effect.

---

## 🔡 Kinetic Typography Rules
- **Legibility First**: Animation must not compromise the readability of the message.
- **Hierarchy**: Use motion to reveal text in order of importance (Heading -> Subhead -> Body).
- **Secondary Action**: Use subtle scale or opacity shifts to support the primary movement.

---

## 🛠 Usage in NEXUS

- **/motion-principles** — Load core animation rules.
- **/motion-principles easing** — Get best easing curves for current context.
- **/motion-principles duration** — Get recommended timings for UI elements.

---

## 📁 Supporting Files
- [patterns.md](patterns.md) — Common UI motion patterns.
- [cheatsheet.md](cheatsheet.md) — GSAP quick reference.
