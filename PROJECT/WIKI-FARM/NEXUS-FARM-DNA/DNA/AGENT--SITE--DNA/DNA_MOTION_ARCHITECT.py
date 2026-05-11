"""
NEXUS DNA: Motion Architect v2.0
Analyzes brand DNA and recommends GSAP animation strategies.

Usage:  python DNA_MOTION_ARCHITECT.py <path_to_dna.json>
Output: motion_strategy.md in the same directory as dna.json
"""

__version__ = "2.0.0"

import json
import re
import sys
from pathlib import Path


def _is_true_serif(font_name: str) -> bool:
    """Return True only for real serif fonts, excluding sans-serif."""
    name = font_name.lower().strip()
    if "sans-serif" in name or "sans serif" in name:
        return False
    if "mono" in name or "code" in name:
        return False
    serif_indicators = [
        "serif", "times", "georgia", "garamond", "playfair",
        "merriweather", "lora", "libre baskerville", "instrument serif",
        "noto serif", "source serif", "dm serif", "cormorant",
    ]
    return any(ind in name for ind in serif_indicators)


def _detect_vibe(dna: dict) -> tuple[str, list[dict]]:
    """Determine brand vibe from DNA signals and return (vibe, recommendations)."""
    colors = dna.get("colors", {})
    typography = dna.get("typography", {})
    animations = dna.get("animations", {})
    accent = dna.get("accent_palette", {})

    # Signal 1: Background brightness
    bg_is_dark = False
    first_bg = colors.get("backgrounds", [{}])[0].get("value", "#FFFFFF")
    if first_bg.startswith("#") and len(first_bg) >= 7:
        r, g, b = int(first_bg[1:3], 16), int(first_bg[3:5], 16), int(first_bg[5:7], 16)
        bg_is_dark = (r * 299 + g * 587 + b * 114) / 1000 < 128

    # Signal 2: Font classification
    fonts = typography.get("families", [])
    has_serif = any(_is_true_serif(f.get("value", "")) for f in fonts)
    primary_font = fonts[0].get("value", "") if fonts else ""

    # Signal 3: Tracking tightness (negative = premium editorial)
    spacings = typography.get("letter_spacings", [])
    has_tight_tracking = any(
        s.get("value", "").startswith("-") and float(s["value"].replace("px", "")) < -1
        for s in spacings if s.get("value", "").replace("-", "").replace(".", "").replace("px", "").isdigit()
    )

    # Signal 4: Animation density on site
    has_animations = bool(animations.get("animations", []))
    has_transitions = bool(animations.get("transitions", []))

    # Signal 5: Accent style (italic = editorial)
    accent_rules = accent.get("accent_rules", [])
    has_italic_accent = any(r.get("font_style") == "italic" for r in accent_rules)

    # Signal 6: Number of gradients (tech/startup indicator)
    gradient_count = len(dna.get("gradients", []))

    # ── Decision Matrix ──
    score_dark_tech = int(bg_is_dark) * 3 + int(gradient_count > 2) * 2 + int(has_animations) * 1
    score_editorial = int(has_serif) * 3 + int(has_italic_accent) * 2 + int(has_tight_tracking) * 2
    score_modern = int(not has_serif and not bg_is_dark) * 2 + int(has_transitions) * 1 + int(gradient_count <= 2) * 1
    score_minimal = int(not has_animations and not has_transitions) * 2 + int(not gradient_count) * 1

    scores = {
        "Premium/Tech": score_dark_tech,
        "Editorial/Classic": score_editorial,
        "Modern/SaaS": score_modern,
        "Minimal/Corporate": score_minimal,
    }
    vibe = max(scores, key=scores.get)

    # ── Recommendation Sets ──
    presets = {
        "Premium/Tech": [
            {"effect": "blurIn", "params": "{ duration: 1.5, amount: 30, ease: 'power2.out' }", "target": "Hero Headlines", "rationale": "Blur-in creates cinematic depth on dark backgrounds."},
            {"effect": "clipRevealY", "params": "{ duration: 1.2, yOffset: 60, ease: 'power4.inOut' }", "target": "Section Titles", "rationale": "Clip-path reveals add premium editorial motion."},
            {"effect": "textReveal", "params": "{ duration: 1, stagger: 0.02, fade: true }", "target": "Main Copy", "rationale": "Word-by-word reveal emphasizes each phrase."},
            {"effect": "parallax", "params": "{ yAmount: -80 }", "target": "Background Images", "rationale": "Depth parallax reinforces the tech-premium feel."},
            {"effect": "glitch", "params": "{ intensity: 2, repeat: 1 }", "target": "Hover Accents", "rationale": "Controlled glitch adds digital edge without chaos."},
        ],
        "Editorial/Classic": [
            {"effect": "fadeUp", "params": "{ duration: 1.2, distance: 30, ease: 'power3.out' }", "target": "Content Blocks", "rationale": "Gentle upward fade matches editorial pacing."},
            {"effect": "textReveal", "params": "{ duration: 1.5, stagger: 0.08, ease: 'expo.out' }", "target": "Headlines", "rationale": "Slow word reveal mirrors reading rhythm."},
            {"effect": "clipRevealX", "params": "{ duration: 1.8, xOffset: -60, ease: 'power4.inOut' }", "target": "Feature Images", "rationale": "Horizontal curtain reveal feels magazine-like."},
            {"effect": "fadeScrub", "params": "{ yOffset: 50 }", "target": "Scroll Sections", "rationale": "Scroll-linked fade keeps attention as user reads."},
            {"effect": "marquee", "params": "{ duration: 15 }", "target": "Ticker / Tagline Bar", "rationale": "Infinite scroll strip adds editorial dynamism."},
        ],
        "Modern/SaaS": [
            {"effect": "fadeUp", "params": "{ duration: 0.8, distance: 40, stagger: 0.1 }", "target": "Feature Cards", "rationale": "Quick staggered reveal feels snappy and modern."},
            {"effect": "scaleIn", "params": "{ duration: 0.6, startScale: 0.9, ease: 'back.out(1.7)' }", "target": "CTA Buttons", "rationale": "Scale bounce draws attention to conversion points."},
            {"effect": "blurIn", "params": "{ duration: 0.8, amount: 15 }", "target": "Hero Section", "rationale": "Subtle blur-in creates polished first impression."},
            {"effect": "makeMagnetic", "params": "power: 30", "target": "Primary CTA", "rationale": "Magnetic hover effect increases click engagement."},
            {"effect": "float", "params": "{ duration: 3, amount: -10 }", "target": "Decorative Icons", "rationale": "Gentle float adds life without distraction."},
        ],
        "Minimal/Corporate": [
            {"effect": "fadeUp", "params": "{ duration: 1, distance: 20, ease: 'power2.out' }", "target": "All Sections", "rationale": "Restrained motion preserves professional tone."},
            {"effect": "fadeLeft", "params": "{ duration: 0.8, distance: 30 }", "target": "Stats / Metrics", "rationale": "Horizontal entrance differentiates data blocks."},
            {"effect": "scaleIn", "params": "{ duration: 0.5, startScale: 0.95, ease: 'power2.out' }", "target": "Cards", "rationale": "Barely-there scale adds polish without flash."},
        ],
    }

    return vibe, presets.get(vibe, presets["Modern/SaaS"]), scores


def _generate_snippet(recommendations: list[dict]) -> str:
    """Generate a ready-to-paste JS implementation snippet."""
    lines = [
        "// ── NEXUS Motion Architect: Auto-Generated ──",
        "import { initGSAPPresets, textReveal, makeMagnetic } from './DNA_GSAP_PRESETS.js';",
        "",
        "// Register all presets",
        "initGSAPPresets(gsap, ScrollTrigger);",
        "",
        "// ── Apply recommendations ──",
    ]
    for rec in recommendations:
        eff = rec["effect"]
        cls = rec["target"].lower().replace(" ", "-").replace("/", "-")
        if eff == "textReveal":
            lines.append(f"textReveal(document.querySelector('.{cls}'), gsap, {rec['params']});")
        elif eff == "makeMagnetic":
            lines.append(f"makeMagnetic(document.querySelector('.{cls}'), gsap, 30);")
        else:
            lines.append(f'gsap.effects.{eff}(".{cls}", {rec["params"]});')
    return "\n".join(lines)


def analyze_motion(dna_path: str) -> Path:
    """Main entry point. Analyze DNA and write motion_strategy.md."""
    dna_file = Path(dna_path)
    if not dna_file.exists():
        print(f"[ERROR] File not found: {dna_file}", file=sys.stderr)
        sys.exit(1)

    dna = json.loads(dna_file.read_text(encoding="utf-8"))
    domain = dna.get("meta", {}).get("domain", "unknown")

    print(f"[NEXUS Motion Architect v{__version__}]", file=sys.stderr)
    print(f"[Analyzing: {domain}]", file=sys.stderr)

    vibe, recommendations, scores = _detect_vibe(dna)

    print(f"[Vibe: {vibe}]", file=sys.stderr)
    print(f"[Scores: {scores}]", file=sys.stderr)

    # ── Build Report ──
    report = [
        f"# Motion Strategy: {domain}",
        f"**Generated by:** NEXUS Motion Architect v{__version__}",
        f"**Vibe detected:** {vibe}",
        "",
        "## Vibe Scores",
        "",
        "| Category | Score |",
        "|---|---|",
    ]
    for cat, sc in sorted(scores.items(), key=lambda x: -x[1]):
        marker = " ◀" if cat == vibe else ""
        report.append(f"| {cat} | **{sc}**{marker} |")

    report.extend(["", "---", "", "## Recommended Animations", ""])

    for i, rec in enumerate(recommendations, 1):
        report.extend([
            f"### {i}. {rec['target']}",
            f"- **Effect:** `{rec['effect']}`",
            f"- **Parameters:** `{rec['params']}`",
            f"- **Rationale:** {rec['rationale']}",
            "",
        ])

    report.extend([
        "---",
        "",
        "## Implementation Snippet",
        "",
        "```javascript",
        _generate_snippet(recommendations),
        "```",
        "",
    ])

    out_path = dna_file.parent / "motion_strategy.md"
    out_path.write_text("\n".join(report), encoding="utf-8")

    print(f"[DONE] {out_path}", file=sys.stderr)
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"NEXUS Motion Architect v{__version__}")
        print("Usage: python DNA_MOTION_ARCHITECT.py <path_to_dna.json>")
        sys.exit(0)
    analyze_motion(sys.argv[1])
