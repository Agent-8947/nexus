"""JS payloads for NEXUS Brand DNA Extractor v4.1"""

# ─── Extract all CSS tokens ──────────────────────────────────────────────
JS_EXTRACT = r"""
() => {
    const cs = (el) => window.getComputedStyle(el);
    const rgbToHex = (s) => {
        const m = s.match(/rgba?\(\s*(\d+),\s*(\d+),\s*(\d+)/);
        if (!m) return null;
        return '#' + [m[1],m[2],m[3]].map(v =>
            parseInt(v).toString(16).padStart(2,'0')).join('').toUpperCase();
    };
    const isVisible = (el) => {
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return false;
        const s = cs(el);
        return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
    };
    const bump = (map, key) => { if (key) map[key] = (map[key] || 0) + 1; };

    const bgColors={},textColors={},borderColors={};
    const fonts={},fontSizes={},fontWeights={};
    const radii={},shadows={},lineHeights={},letterSpacings={},paddings={};
    const gradients=[],gradientSet=new Set();

    for (const el of document.querySelectorAll('*')) {
        if (!isVisible(el)) continue;
        const s = cs(el);
        const bg = rgbToHex(s.backgroundColor);
        if (bg && s.backgroundColor !== 'rgba(0, 0, 0, 0)') bump(bgColors, bg);
        bump(textColors, rgbToHex(s.color));
        const bc = rgbToHex(s.borderColor || s.borderTopColor);
        if (bc && s.borderWidth !== '0px' && s.borderStyle !== 'none') bump(borderColors, bc);
        const family = s.fontFamily.split(',')[0].trim().replace(/['"]/g, '');
        bump(fonts, family);
        bump(fontSizes, s.fontSize);
        bump(fontWeights, s.fontWeight);
        bump(lineHeights, s.lineHeight);
        if (s.letterSpacing !== 'normal') bump(letterSpacings, s.letterSpacing);
        if (s.borderRadius && s.borderRadius !== '0px') bump(radii, s.borderRadius);
        if (s.boxShadow && s.boxShadow !== 'none') bump(shadows, s.boxShadow);
        const bi = s.backgroundImage;
        if (bi && bi !== 'none' && bi.includes('gradient') && !gradientSet.has(bi)) {
            gradientSet.add(bi); gradients.push(bi);
        }
        if (s.padding && s.padding !== '0px') bump(paddings, s.padding);
    }

    const sorted = (obj, n=25) => Object.entries(obj)
        .sort((a,b) => b[1] - a[1]).slice(0, n)
        .map(([value, count]) => ({ value, count }));

    return {
        colors: { backgrounds: sorted(bgColors), text: sorted(textColors), borders: sorted(borderColors) },
        typography: { families: sorted(fonts, 10), sizes: sorted(fontSizes, 15),
            weights: sorted(fontWeights), line_heights: sorted(lineHeights, 10),
            letter_spacings: sorted(letterSpacings, 10) },
        geometry: { border_radii: sorted(radii), box_shadows: sorted(shadows, 10) },
        spacing: { paddings: sorted(paddings, 15) },
        gradients: gradients.slice(0, 10)
    };
}
"""

# ─── Accent style extraction (composite rules) ──────────────────────────
JS_ACCENT = r"""
() => {
    const cs = (el) => window.getComputedStyle(el);
    const rgbToHex = (s) => {
        const m = s.match(/rgba?\(\s*(\d+),\s*(\d+),\s*(\d+)/);
        if (!m) return null;
        return '#' + [m[1],m[2],m[3]].map(v =>
            parseInt(v).toString(16).padStart(2,'0')).join('').toUpperCase();
    };
    const cleanFont = (s) => s.fontFamily.split(',')[0].trim().replace(/['"]/g,'');

    // ── Step 1: detect primary font ──
    const fontFreq = {};
    document.querySelectorAll('*').forEach(el => {
        fontFreq[cleanFont(cs(el))] = (fontFreq[cleanFont(cs(el))]||0) + 1;
    });
    const primary_font = Object.entries(fontFreq).sort((a,b)=>b[1]-a[1])[0]?.[0] || '';

    // ── Step 2: extract COMPOSITE accent rules from headings ──
    // For each inline child (span/em/i/b/strong) inside h1-h4,
    // compare its computed style to the parent heading.
    // If ANY property differs, record the full style tuple.
    const ruleMap = {};  // key = "font|style|weight|color" -> {rule, score, samples}

    document.querySelectorAll('h1,h2,h3,h4').forEach(h => {
        const ps = cs(h);
        const parentFont = cleanFont(ps);
        const parentColor = rgbToHex(ps.color);
        const parentStyle = ps.fontStyle;
        const parentWeight = ps.fontWeight;
        const parentLetterSpacing = ps.letterSpacing;
        const parentLineHeight = ps.lineHeight;
        const parentTextTransform = ps.textTransform;
        const parentFontSize = ps.fontSize;

        h.querySelectorAll('span,em,strong,i,b').forEach(child => {
            const s = cs(child);
            const childFont = cleanFont(s);
            const childColor = rgbToHex(s.color);
            const childStyle = s.fontStyle;
            const childWeight = s.fontWeight;
            const childLetterSpacing = s.letterSpacing;
            const childLineHeight = s.lineHeight;
            const childTextTransform = s.textTransform;

            // Check if child differs from parent in any way
            const fontDiff = childFont !== parentFont;
            const colorDiff = childColor !== parentColor;
            const styleDiff = childStyle !== parentStyle;
            const weightDiff = childWeight !== parentWeight;
            const trackingDiff = childLetterSpacing !== parentLetterSpacing;

            if (fontDiff || colorDiff || styleDiff || weightDiff || trackingDiff) {
                const key = `${childFont}|${childStyle}|${childWeight}|${childColor}|${childLetterSpacing}`;
                if (!ruleMap[key]) {
                    ruleMap[key] = {
                        font_family: childFont,
                        font_style: childStyle,
                        font_weight: childWeight,
                        color: childColor,
                        letter_spacing: childLetterSpacing,
                        line_height: childLineHeight,
                        text_transform: childTextTransform,
                        parent_font_size: parentFontSize,
                        differs_from_parent: {
                            font: fontDiff,
                            color: colorDiff,
                            style: styleDiff,
                            weight: weightDiff,
                            tracking: trackingDiff
                        },
                        score: 0,
                        samples: [],
                        context: 'heading_inline'
                    };
                }
                ruleMap[key].score += 5;
                const txt = child.textContent.trim().slice(0,50);
                if (txt && ruleMap[key].samples.length < 5 && !ruleMap[key].samples.includes(txt)) {
                    ruleMap[key].samples.push(txt);
                }
            }
        });
    });

    // ── Step 3: detect accent usage on standalone elements ──
    // Elements using non-primary fonts that appear < 100 times
    document.querySelectorAll('*').forEach(el => {
        const s = cs(el);
        const f = cleanFont(s);
        if (f !== primary_font && (fontFreq[f]||0) < 100 && (fontFreq[f]||0) > 1) {
            const color = rgbToHex(s.color);
            const key = `${f}|${s.fontStyle}|${s.fontWeight}|${color}`;
            if (!ruleMap[key]) {
                ruleMap[key] = {
                    font_family: f,
                    font_style: s.fontStyle,
                    font_weight: s.fontWeight,
                    color: color,
                    differs_from_parent: { font: true, color: false, style: false, weight: false },
                    score: 0,
                    samples: [],
                    context: 'standalone'
                };
            }
            ruleMap[key].score += 1;
        }
    });

    // ── Step 4: button composite styles ──
    const button_styles = [];
    const btnSeen = new Set();
    document.querySelectorAll('button,a[class*="btn"],a[class*="button"],[role="button"],input[type="submit"]').forEach(el => {
        const s = cs(el);
        const bg = rgbToHex(s.backgroundColor);
        const color = rgbToHex(s.color);
        const font = cleanFont(s);
        const key = `${bg}|${color}|${s.borderRadius}|${font}`;
        if (!btnSeen.has(key)) {
            btnSeen.add(key);
            button_styles.push({
                background: bg,
                color: color,
                font_family: font,
                font_weight: s.fontWeight,
                font_size: s.fontSize,
                letter_spacing: s.letterSpacing,
                line_height: s.lineHeight,
                text_transform: s.textTransform,
                border_radius: s.borderRadius,
                padding: s.padding,
                text: el.textContent.trim().slice(0,40)
            });
        }
    });

    // ── Step 5: badge/pill composite styles ──
    const badge_styles = [];
    const badgeSeen = new Set();
    document.querySelectorAll('span,div,p,a').forEach(el => {
        const s = cs(el);
        const r = el.getBoundingClientRect();
        if (r.width > 20 && r.width < 300 && r.height > 10 && r.height < 60) {
            const radius = parseFloat(s.borderRadius) || 0;
            if (radius > 16) {
                const bg = rgbToHex(s.backgroundColor);
                const color = rgbToHex(s.color);
                const key = `${bg}|${color}|${s.fontSize}`;
                if (!badgeSeen.has(key) && (bg || color)) {
                    badgeSeen.add(key);
                    badge_styles.push({
                        background: bg,
                        color: color,
                        font_size: s.fontSize,
                        font_weight: s.fontWeight,
                        border_radius: s.borderRadius,
                        text: el.textContent.trim().slice(0,30)
                    });
                }
            }
        }
    });

    // ── Sort accent_rules by score ──
    const accent_rules = Object.values(ruleMap)
        .sort((a,b) => b.score - a.score)
        .slice(0, 10);

    return {
        primary_font,
        accent_rules,
        button_styles: button_styles.slice(0, 10),
        badge_styles: badge_styles.slice(0, 10)
    };
}
"""

# ─── Logo candidates ─────────────────────────────────────────────────────
JS_LOGO = r"""
() => {
    const candidates = [];
    document.querySelectorAll('header svg, nav svg, [class*="logo"] svg, [id*="logo"] svg, a[href="/"] svg').forEach(svg => {
        const clone = svg.cloneNode(true);
        const w = svg.getBoundingClientRect().width;
        const h = svg.getBoundingClientRect().height;
        if (w > 20 && w < 400 && h > 10 && h < 200) {
            if (!clone.getAttribute('xmlns')) clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            if (!clone.getAttribute('width')) clone.setAttribute('width', Math.round(w));
            if (!clone.getAttribute('height')) clone.setAttribute('height', Math.round(h));
            candidates.push({ type: 'svg', data: clone.outerHTML, w: Math.round(w), h: Math.round(h) });
        }
    });
    document.querySelectorAll('header img, nav img, [class*="logo"] img, [id*="logo"] img, a[href="/"] img').forEach(img => {
        const w = img.naturalWidth || img.width;
        const h = img.naturalHeight || img.height;
        if (w > 20 && w < 800 && h > 10 && h < 400) {
            candidates.push({ type: 'img', data: img.src, w, h });
        }
    });
    return candidates;
}
"""

# ─── Internal links ──────────────────────────────────────────────────────
JS_LINKS = r"""
(origin) => {
    const urls = new Set();
    document.querySelectorAll('a[href]').forEach(a => {
        try {
            const u = new URL(a.href, origin);
            if (u.origin === origin && !u.hash && !u.href.match(/\.(pdf|png|jpg|svg|zip|mp4)$/i))
                urls.add(u.pathname);
        } catch(_) {}
    });
    return Array.from(urls);
}
"""

# ─── Favicon ──────────────────────────────────────────────────────────────
JS_FAVICON = r"""
() => {
    const icons = [];
    document.querySelectorAll('link[rel*="icon"]').forEach(link => {
        icons.push({ href: link.href, type: link.type || '', sizes: link.sizes?.value || '' });
    });
    return icons;
}
"""

# ─── OG / Meta ────────────────────────────────────────────────────────────
JS_OG_META = r"""
() => {
    const meta = {};
    meta.title = document.title || '';
    const desc = document.querySelector('meta[name="description"]');
    if (desc) meta.description = desc.content;
    document.querySelectorAll('meta[property^="og:"]').forEach(m => {
        meta[m.getAttribute('property')] = m.content;
    });
    document.querySelectorAll('meta[name^="twitter:"]').forEach(m => {
        meta[m.getAttribute('name')] = m.content;
    });
    return meta;
}
"""

# ─── All inline SVG icons ────────────────────────────────────────────────
JS_ICONS = r"""
() => {
    const icons = [];
    const seen = new Set();
    document.querySelectorAll('svg').forEach(svg => {
        const w = svg.getBoundingClientRect().width;
        const h = svg.getBoundingClientRect().height;
        if (w >= 12 && w <= 48 && h >= 12 && h <= 48) {
            const clone = svg.cloneNode(true);
            if (!clone.getAttribute('xmlns')) clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            clone.setAttribute('width', Math.round(w));
            clone.setAttribute('height', Math.round(h));
            const html = clone.outerHTML;
            const key = html.length + '_' + w + '_' + h;
            if (!seen.has(key)) {
                seen.add(key);
                icons.push({ svg: html, w: Math.round(w), h: Math.round(h) });
            }
        }
    });
    return icons;
}
"""

# ─── CSS Animations & Transitions ────────────────────────────────────────
JS_ANIMATIONS = r"""
() => {
    const transitions = {};
    const easings = {};
    const animations = {};
    const bump = (map, key) => { if (key && key !== 'none' && key !== '0s') map[key] = (map[key] || 0) + 1; };

    for (const el of document.querySelectorAll('*')) {
        const s = window.getComputedStyle(el);
        if (s.transitionDuration && s.transitionDuration !== '0s')
            bump(transitions, s.transitionDuration);
        if (s.transitionTimingFunction && s.transitionTimingFunction !== 'ease')
            bump(easings, s.transitionTimingFunction);
        if (s.animationName && s.animationName !== 'none')
            bump(animations, s.animationName + ' ' + s.animationDuration);
    }

    const sorted = (obj) => Object.entries(obj).sort((a,b) => b[1] - a[1]).slice(0,10)
        .map(([value, count]) => ({ value, count }));

    return { transitions: sorted(transitions), easings: sorted(easings), animations: sorted(animations) };
}
"""

# ─── Button variants ─────────────────────────────────────────────────────
JS_BUTTONS = r"""
() => {
    const cs = (el) => window.getComputedStyle(el);
    const rgbToHex = (s) => {
        const m = s.match(/rgba?\(\s*(\d+),\s*(\d+),\s*(\d+)/);
        if (!m) return s;
        return '#' + [m[1],m[2],m[3]].map(v => parseInt(v).toString(16).padStart(2,'0')).join('').toUpperCase();
    };
    const btns = [];
    const seen = new Set();
    document.querySelectorAll('button, a[class*="btn"], a[class*="button"], [role="button"], input[type="submit"]').forEach(el => {
        const s = cs(el);
        const key = rgbToHex(s.backgroundColor) + '|' + rgbToHex(s.color) + '|' + s.borderRadius + '|' + s.padding;
        if (seen.has(key)) return;
        seen.add(key);
        btns.push({
            text: el.textContent.trim().slice(0, 40),
            bg: rgbToHex(s.backgroundColor),
            color: rgbToHex(s.color),
            border: s.border,
            radius: s.borderRadius,
            padding: s.padding,
            fontSize: s.fontSize,
            fontWeight: s.fontWeight
        });
    });
    return btns.slice(0, 15);
}
"""

# ─── Layout patterns ─────────────────────────────────────────────────────
JS_LAYOUT = r"""
() => {
    const cs = (el) => window.getComputedStyle(el);
    const maxWidths = {};
    const gaps = {};
    const bump = (map, key) => { if (key && key !== 'none' && key !== '0px' && key !== 'normal') map[key] = (map[key] || 0) + 1; };

    document.querySelectorAll('div, section, main, article, header, footer').forEach(el => {
        const s = cs(el);
        if (s.maxWidth && s.maxWidth !== 'none') bump(maxWidths, s.maxWidth);
        if (s.gap && s.gap !== 'normal' && s.gap !== '0px') bump(gaps, s.gap);
    });

    const sorted = (obj) => Object.entries(obj).sort((a,b) => b[1] - a[1]).slice(0,10)
        .map(([value, count]) => ({ value, count }));

    return { max_widths: sorted(maxWidths), gaps: sorted(gaps) };
}
"""

# ─── Images ───────────────────────────────────────────────────────────────
JS_IMAGES = r"""
() => {
    const imgs = [];
    const seen = new Set();
    document.querySelectorAll('img[src]').forEach(img => {
        const src = img.src;
        if (seen.has(src) || src.startsWith('data:')) return;
        seen.add(src);
        const w = img.naturalWidth || img.width;
        const h = img.naturalHeight || img.height;
        if (w > 80 && h > 80) {
            imgs.push({ src, w, h, alt: img.alt || '' });
        }
    });
    return imgs.slice(0, 20);
}
"""

# ─── Copy DNA (headings, CTAs, paragraphs) ───────────────────────────────
JS_COPY = r"""
() => {
    const data = { headings: [], ctas: [], paragraphs: [], tagline: '' };

    document.querySelectorAll('h1, h2, h3').forEach(h => {
        const text = h.textContent.trim().replace(/\s+/g, ' ');
        if (text.length > 2 && text.length < 200)
            data.headings.push({ tag: h.tagName, text });
    });

    document.querySelectorAll('button, a[class*="btn"], a[class*="button"], [role="button"]').forEach(el => {
        const text = el.textContent.trim().replace(/\s+/g, ' ');
        if (text.length > 1 && text.length < 60)
            data.ctas.push(text);
    });

    document.querySelectorAll('p').forEach(p => {
        const text = p.textContent.trim().replace(/\s+/g, ' ');
        if (text.length > 30 && text.length < 500)
            data.paragraphs.push(text);
    });

    // Tagline: first short paragraph or first h2 after h1
    const hero = document.querySelector('h1');
    if (hero) {
        const next = hero.nextElementSibling;
        if (next && (next.tagName === 'P' || next.tagName === 'H2')) {
            data.tagline = next.textContent.trim().replace(/\s+/g, ' ');
        }
    }

    return data;
}
"""
