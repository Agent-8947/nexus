# NEXUS Business Animations v3.0

Production-grade GSAP animation library for premium business websites.

## Quick Start

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script type="module">
import { initNexusAnimations, makeMagnetic, countUp, customCursor, curtainIn }
    from './NEXUS_BUSINESS_ANIMATIONS.js';

gsap.registerPlugin(ScrollTrigger);
initNexusAnimations(gsap, ScrollTrigger);
curtainIn(gsap);
customCursor(gsap);
</script>
```

## 21 Presets

| # | Name | Type | Use Case |
|---|---|---|---|
| 1 | `wordReveal` | Text | Hero H1/H2 — words slide up |
| 2 | `charReveal` | Text | Logos — letters fade in |
| 3 | `lineReveal` | Text | Subtitles — clip-path wipe |
| 4 | `typewriter` | Text (fn) | Terminal — char-by-char + cursor |
| 5 | `headingSplit` | Text | Agency — halves from opposite sides |
| 6 | `revealUp` | Scroll | Standard content appear |
| 7 | `revealStagger` | Scroll | Cards/grids — cascading |
| 8 | `revealImage` | Scroll | Awwwards — clip + inner scale |
| 9 | `revealLine` | Scroll | Dividers — draws left→right |
| 10 | `countUp` | Stats (fn) | Numbers — 0 to target |
| 11 | `progressBar` | Stats | Skill bars — scaleX |
| 12 | `parallaxSection` | Mechanics | Hero bg — depth scroll |
| 13 | `horizontalScroll` | Mechanics | Portfolio — pin + X scroll |
| 14 | `stickyReveal` | Mechanics | SaaS features — Linear-style |
| 15 | `makeMagnetic` | UI (fn) | CTA buttons — cursor follow |
| 16 | `hoverUnderline` | UI (fn) | Nav links — enter L, exit R |
| 17 | `customCursor` | UI (fn) | Agency — ring + dot |
| 18 | `buttonHover` | UI (fn) | Primary CTA — double text |
| 19 | `cardTilt` | UI (fn) | Pricing — 3D perspective |
| 20 | `curtainIn` | Transition (fn) | Page entry — black overlay |
| 21 | `curtainOut` | Transition (fn) | Page exit — overlay + navigate |

## Files

```
nexus-animations/
├── NEXUS_BUSINESS_ANIMATIONS.js   ← Library (ES module)
├── NEXUS_ANIMATIONS_DEMO.html     ← Interactive demo
└── README.md
```
