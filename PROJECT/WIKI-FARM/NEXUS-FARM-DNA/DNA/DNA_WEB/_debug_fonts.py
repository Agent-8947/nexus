from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width":1440,"height":900})
    pg.goto("https://solaraimpact.ai/", wait_until="load", timeout=30000)
    pg.wait_for_timeout(3000)

    # Check what fonts are LOADED via document.fonts API
    fonts = pg.evaluate("""() => {
        const loaded = [];
        document.fonts.forEach(f => loaded.push({
            family: f.family,
            style: f.style,
            weight: f.weight,
            status: f.status
        }));
        return loaded;
    }""")
    print("=== LOADED FONTS ===")
    for f in fonts:
        print(f"  {f['family']} | style={f['style']} weight={f['weight']} status={f['status']}")

    # Check what stylesheets declare
    css_fonts = pg.evaluate("""() => {
        const results = [];
        for (const sheet of document.styleSheets) {
            try {
                for (const rule of sheet.cssRules) {
                    if (rule.type === CSSRule.FONT_FACE_RULE) {
                        results.push(rule.cssText.slice(0, 200));
                    }
                }
            } catch(e) {}
        }
        return results;
    }""")
    print("\n=== @font-face RULES ===")
    for r in css_fonts[:10]:
        print(f"  {r}")

    # Check computed style on accent elements inside headings
    accents = pg.evaluate("""() => {
        const results = [];
        document.querySelectorAll('h1, h2').forEach(h => {
            h.querySelectorAll('span, em, i, b, strong').forEach(child => {
                const s = window.getComputedStyle(child);
                const ps = window.getComputedStyle(h);
                results.push({
                    parent_tag: h.tagName,
                    child_tag: child.tagName,
                    text: child.textContent.trim().slice(0, 50),
                    child_fontFamily: s.fontFamily,
                    child_fontStyle: s.fontStyle,
                    child_color: s.color,
                    parent_fontFamily: ps.fontFamily,
                    parent_fontStyle: ps.fontStyle,
                    parent_color: ps.color
                });
            });
        });
        return results.slice(0, 10);
    }""")
    print("\n=== ACCENT ELEMENTS IN HEADINGS ===")
    for a in accents:
        print(json.dumps(a, indent=2))

    b.close()
