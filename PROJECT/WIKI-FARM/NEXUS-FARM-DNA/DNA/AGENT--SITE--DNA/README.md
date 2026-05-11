# AGENT -- SITE -- DNA
**Autonomous Brand DNA Extraction & Motion Architecture** [NEXUS v5.0 Production]

---

## Architecture

```
run.py                       ← Unified entry point (Extract → Analyze → Recommend)
├── nexus_visual_analyzer.py ← Core extractor (Playwright + JS DOM injection)
│   └── js_payloads.py       ← 11 JS payloads: tokens, accents, copy, layout, animations
├── DNA_MOTION_ARCHITECT.py  ← Vibe detector + animation strategy generator
└── DNA_GSAP_PRESETS.js      ← 20 production GSAP presets (ready to embed)
```

## Quick Start

```powershell
# Install
pip install -r requirements.txt
python -m playwright install chromium

# Full pipeline (extract + motion strategy)
python run.py https://example.com

# Custom output directory
python run.py https://example.com --output ./brands

# Scan more pages
python run.py https://example.com --pages 8

# Motion strategy only (from existing DNA)
python run.py --motion ./output/BRAND_001_example/dna.json
```

## Output Structure

```
output/BRAND_NNN_<domain>/
├── dna.json             ← Machine-readable design system
├── brandbook.html       ← Visual report (colors, fonts, tracking, accents)
├── copy_dna.md          ← Tone analysis + web scenario
├── motion_strategy.md   ← Animation recommendations + JS snippets
├── screenshot.png       ← Homepage capture
├── logo.svg             ← Extracted vector logo
├── favicon_*.{ico,png}  ← Favicon variants
├── icons/               ← All inline SVG icons
└── images/              ← Key images (up to 5 per page)
```

## What Gets Extracted

| Layer | Metrics |
|---|---|
| **Colors** | Backgrounds, text, borders, gradients |
| **Typography** | Families, sizes, weights, **letter-spacing**, **line-height** |
| **Accents** | Inline style rules (font, style, weight, color, tracking) |
| **Geometry** | Border radii, box shadows, paddings |
| **Buttons** | Full composite style (bg, color, radius, font, tracking) |
| **Layout** | Max-widths, gaps |
| **Animations** | Transitions, easings, CSS animations |
| **Copy DNA** | Headings, CTAs, paragraphs, tagline, brand voice |
| **Motion** | Vibe detection → 4-5 GSAP preset recommendations |

## Dependencies

- **Python 3.10+**
- **Playwright** (chromium) — headless browser for DOM extraction

---

*NEXUS Brand DNA Extractor — Production Edition*
