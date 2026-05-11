/**
 * NEXUS Business Animations v3.0 — Production-Grade GSAP Library
 * Premium minimalist animations for Agency / SaaS / Corporate / Landing pages.
 *
 * Usage:
 *   import { initNexusAnimations, makeMagnetic, hoverUnderline,
 *            customCursor, buttonHover, cardTilt, curtainIn, curtainOut,
 *            countUp } from './NEXUS_BUSINESS_ANIMATIONS.js';
 *   initNexusAnimations(gsap, ScrollTrigger);
 */

// ─── UTILITY: Split text into wrapped spans ─────────────────────────────
function splitWords(element) {
    const text = element.textContent;
    element.innerHTML = '';
    const words = text.split(/\s+/).filter(Boolean);
    const spans = [];
    words.forEach(word => {
        const wrapper = document.createElement('span');
        wrapper.style.display = 'inline-block';
        wrapper.style.overflow = 'hidden';
        wrapper.style.verticalAlign = 'top';
        const inner = document.createElement('span');
        inner.style.display = 'inline-block';
        inner.textContent = word + '\u00A0';
        wrapper.appendChild(inner);
        element.appendChild(wrapper);
        spans.push(inner);
    });
    return spans;
}

function splitChars(element) {
    const text = element.textContent;
    element.innerHTML = '';
    const chars = [];
    for (const ch of text) {
        const span = document.createElement('span');
        span.style.display = 'inline-block';
        if (ch === ' ') { span.innerHTML = '&nbsp;'; }
        else { span.textContent = ch; }
        element.appendChild(span);
        chars.push(span);
    }
    return chars;
}

// ═══════════════════════════════════════════════════════════════════════════
// MAIN INIT
// ═══════════════════════════════════════════════════════════════════════════
export const initNexusAnimations = (gsap, ScrollTrigger = null) => {

    // ─── I. TEXT REVEALS ────────────────────────────────────────────────

    /**
     * 1. wordReveal — Hero headings. Splits into words, each slides up from below.
     * Usage: gsap.effects.wordReveal(".hero-title");
     */
    gsap.registerEffect({
        name: "wordReveal",
        effect: (targets, config) => {
            const tl = gsap.timeline();
            targets.forEach(el => {
                const words = splitWords(el);
                tl.from(words, {
                    yPercent: 110,
                    duration: config.duration,
                    ease: config.ease,
                    stagger: config.stagger,
                    clearProps: "all"
                }, 0);
            });
            return tl;
        },
        defaults: { duration: 1.1, ease: "power4.out", stagger: 0.06 },
        extendTimeline: true
    });

    /**
     * 2. charReveal — Short accent phrases, logos. Letter-by-letter fade up.
     * Usage: gsap.effects.charReveal(".logo-text", { duration: 0.5 });
     */
    gsap.registerEffect({
        name: "charReveal",
        effect: (targets, config) => {
            const tl = gsap.timeline();
            targets.forEach(el => {
                const chars = splitChars(el);
                tl.from(chars, {
                    opacity: 0, y: 20,
                    duration: config.duration,
                    ease: config.ease,
                    stagger: config.stagger,
                    clearProps: "all"
                }, 0);
            });
            return tl;
        },
        defaults: { duration: 0.7, ease: "power3.out", stagger: 0.025 },
        extendTimeline: true
    });

    /**
     * 3. lineReveal — Subtitles, captions. Clip-path wipe left-to-right.
     * Usage: gsap.effects.lineReveal(".section-subtitle");
     */
    gsap.registerEffect({
        name: "lineReveal",
        effect: (targets, config) => gsap.fromTo(targets,
            { clipPath: "inset(0 100% 0 0)" },
            { clipPath: "inset(0 0% 0 0)", duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "clipPath" }
        ),
        defaults: { duration: 1.4, ease: "power4.inOut", stagger: 0 },
        extendTimeline: true
    });

    /**
     * 4. headingSplit — Agency hero. Splits heading in half, halves slide from opposite sides.
     * Usage: gsap.effects.headingSplit(".split-heading");
     */
    gsap.registerEffect({
        name: "headingSplit",
        effect: (targets, config) => {
            const tl = gsap.timeline();
            targets.forEach(el => {
                const text = el.textContent;
                const mid = Math.ceil(text.length / 2);
                const leftText = text.slice(0, mid).trimEnd();
                const rightText = text.slice(mid).trimStart();
                el.innerHTML = '';
                const leftSpan = document.createElement('span');
                leftSpan.style.display = 'inline-block';
                leftSpan.textContent = leftText + ' ';
                const rightSpan = document.createElement('span');
                rightSpan.style.display = 'inline-block';
                rightSpan.textContent = rightText;
                el.appendChild(leftSpan);
                el.appendChild(rightSpan);
                tl.from(leftSpan, { x: -config.distance, opacity: 0, duration: config.duration, ease: config.ease, clearProps: "all" }, 0);
                tl.from(rightSpan, { x: config.distance, opacity: 0, duration: config.duration, ease: config.ease, clearProps: "all" }, 0);
            });
            return tl;
        },
        defaults: { duration: 1.2, distance: 60, ease: "expo.out" },
        extendTimeline: true
    });

    // ─── II. SCROLL REVEALS ────────────────────────────────────────────

    /**
     * 6. revealUp — Standard content reveal. Cards, text, images.
     * Usage: gsap.effects.revealUp(".section-text");
     */
    gsap.registerEffect({
        name: "revealUp",
        effect: (targets, config) => {
            if (ScrollTrigger) {
                return gsap.from(targets, {
                    y: config.distance, opacity: 0,
                    duration: config.duration, ease: config.ease,
                    stagger: config.stagger,
                    clearProps: "all",
                    scrollTrigger: { trigger: targets[0], start: "top 85%", once: true }
                });
            }
            return gsap.from(targets, { y: config.distance, opacity: 0, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "all" });
        },
        defaults: { duration: 0.9, distance: 60, ease: "power3.out", stagger: 0 },
        extendTimeline: true
    });

    /**
     * 7. revealStagger — Groups: cards, features, team grids. Cascading entrance.
     * Usage: gsap.effects.revealStagger(".feature-card");
     */
    gsap.registerEffect({
        name: "revealStagger",
        effect: (targets, config) => {
            if (ScrollTrigger) {
                return gsap.from(targets, {
                    y: 40, opacity: 0,
                    duration: config.duration, ease: config.ease,
                    stagger: config.stagger,
                    clearProps: "all",
                    scrollTrigger: { trigger: targets[0], start: "top 80%", once: true }
                });
            }
            return gsap.from(targets, { y: 40, opacity: 0, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "all" });
        },
        defaults: { duration: 0.9, ease: "power3.out", stagger: 0.12 },
        extendTimeline: true
    });

    /**
     * 8. revealImage — Awwwards-grade image reveal. Clip-path + inner scale.
     * Usage: gsap.effects.revealImage(".hero-image");
     */
    gsap.registerEffect({
        name: "revealImage",
        effect: (targets, config) => {
            const tl = gsap.timeline();
            targets.forEach(el => {
                const img = el.querySelector('img') || el;
                tl.fromTo(el,
                    { clipPath: "polygon(0 100%, 100% 100%, 100% 100%, 0 100%)" },
                    { clipPath: "polygon(0 0%, 100% 0%, 100% 100%, 0 100%)", duration: config.duration, ease: config.ease, clearProps: "clipPath" }, 0
                );
                if (img !== el) {
                    tl.from(img, { scale: 1.15, duration: config.duration * 1.2, ease: config.ease, clearProps: "transform" }, 0);
                }
            });
            if (ScrollTrigger) {
                ScrollTrigger.create({ trigger: targets[0], start: "top 85%", once: true, animation: tl });
            }
            return tl;
        },
        defaults: { duration: 1.4, ease: "power4.inOut" },
        extendTimeline: true
    });

    /**
     * 9. revealLine — Decorative section dividers. Draws left-to-right.
     * Usage: gsap.effects.revealLine(".divider");
     */
    gsap.registerEffect({
        name: "revealLine",
        effect: (targets, config) => {
            if (ScrollTrigger) {
                return gsap.from(targets, {
                    scaleX: 0, transformOrigin: "left center",
                    duration: config.duration, ease: config.ease,
                    clearProps: "all",
                    scrollTrigger: { trigger: targets[0], start: "top 85%", once: true }
                });
            }
            return gsap.from(targets, { scaleX: 0, transformOrigin: "left center", duration: config.duration, ease: config.ease, clearProps: "all" });
        },
        defaults: { duration: 1.0, ease: "power3.inOut" },
        extendTimeline: true
    });

    // ─── III. STATS & NUMBERS ──────────────────────────────────────────

    /**
     * 11. progressBar — Skill bars, funding progress. Scales from 0 to target%.
     * Usage: gsap.effects.progressBar(".skill-bar", { target: 85 });
     */
    gsap.registerEffect({
        name: "progressBar",
        effect: (targets, config) => {
            if (ScrollTrigger) {
                return gsap.fromTo(targets,
                    { scaleX: 0, transformOrigin: "left center" },
                    { scaleX: config.target / 100, duration: config.duration, ease: config.ease, clearProps: "none",
                      scrollTrigger: { trigger: targets[0], start: "top 85%", once: true } }
                );
            }
            return gsap.fromTo(targets, { scaleX: 0, transformOrigin: "left center" }, { scaleX: config.target / 100, duration: config.duration, ease: config.ease });
        },
        defaults: { duration: 1.5, target: 100, ease: "power3.out" },
        extendTimeline: true
    });

    // ─── IV. SCROLL MECHANICS ──────────────────────────────────────────

    if (ScrollTrigger) {
        /**
         * 12. parallaxSection — Hero backgrounds. Smooth depth parallax.
         * Usage: gsap.effects.parallaxSection(".hero-bg");
         */
        gsap.registerEffect({
            name: "parallaxSection",
            effect: (targets, config) => gsap.fromTo(targets,
                { y: -config.amount },
                { y: config.amount, ease: "none", scrollTrigger: { trigger: config.trigger || targets[0], start: "top bottom", end: "bottom top", scrub: config.scrub } }
            ),
            defaults: { amount: 80, scrub: 1.5, trigger: null },
            extendTimeline: false
        });

        /**
         * 13. horizontalScroll — Portfolio, feature showcase. Pins section, scrolls children horizontally.
         * Usage: gsap.effects.horizontalScroll(".portfolio-track");
         */
        gsap.registerEffect({
            name: "horizontalScroll",
            effect: (targets, config) => {
                const track = targets[0];
                const container = config.container ? document.querySelector(config.container) : track.parentElement;
                const scrollWidth = track.scrollWidth - window.innerWidth;
                return gsap.to(track, {
                    x: -scrollWidth,
                    ease: "none",
                    scrollTrigger: { trigger: container, start: "top top", end: () => `+=${scrollWidth}`, scrub: config.scrub, pin: true, anticipatePin: 1 }
                });
            },
            defaults: { scrub: 1, container: null },
            extendTimeline: false
        });

        /**
         * 14. stickyReveal — SaaS feature lists (Linear-style). Pins section, reveals children sequentially.
         * Usage: gsap.effects.stickyReveal(".features-list");
         */
        gsap.registerEffect({
            name: "stickyReveal",
            effect: (targets, config) => {
                const section = targets[0];
                const children = Array.from(section.children);
                const tl = gsap.timeline({
                    scrollTrigger: { trigger: section, start: "top top", end: () => `+=${children.length * config.spacing}`, scrub: 1, pin: true }
                });
                children.forEach((child, i) => {
                    if (i > 0) {
                        tl.fromTo(child, { opacity: 0.2, scale: 0.95 }, { opacity: 1, scale: 1, duration: 1, ease: "power2.out", clearProps: "all" });
                    }
                });
                return tl;
            },
            defaults: { spacing: 300 },
            extendTimeline: false
        });
    }
}; // end initNexusAnimations


// ═══════════════════════════════════════════════════════════════════════════
// V. UI INTERACTIONS (standalone functions)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * 10. countUp — Animates a number from 0 to target with suffix.
 * Usage: countUp(".stat-number", gsap, { suffix: "%", ScrollTrigger });
 * @param {string|Element} selector
 * @param {object} gsap
 * @param {object} config - { duration, suffix, separator, ease, ScrollTrigger }
 */
export const countUp = (selector, gsap, config = {}) => {
    const elements = typeof selector === 'string' ? document.querySelectorAll(selector) : [selector];
    const duration = config.duration || 2.0;
    const ease = config.ease || "power2.out";
    const suffix = config.suffix || "";
    const separator = config.separator !== false;
    const ST = config.ScrollTrigger || null;

    elements.forEach(el => {
        const rawText = el.textContent.replace(/[^0-9.]/g, '');
        const target = parseFloat(rawText) || 0;
        const isFloat = rawText.includes('.');
        const decimals = isFloat ? (rawText.split('.')[1] || '').length : 0;
        const obj = { val: 0 };

        const anim = gsap.to(obj, {
            val: target,
            duration,
            ease,
            paused: !!(ST),
            onUpdate: () => {
                let v = isFloat ? obj.val.toFixed(decimals) : Math.round(obj.val);
                if (separator && !isFloat) {
                    v = Number(v).toLocaleString('en-US');
                }
                el.textContent = v + suffix;
            }
        });

        if (ST) {
            ST.create({ trigger: el, start: "top 85%", once: true, onEnter: () => anim.play() });
        }
    });
};

/**
 * 4. typewriter — Terminal-style character reveal with blinking cursor.
 * Usage: typewriter(".hero-tagline", gsap, { charDelay: 0.04 });
 */
export const typewriter = (selector, gsap, config = {}) => {
    const elements = typeof selector === 'string' ? document.querySelectorAll(selector) : [selector];
    const charDelay = config.charDelay || 0.04;

    elements.forEach(el => {
        const text = el.textContent;
        el.textContent = '';
        const cursor = document.createElement('span');
        cursor.textContent = '|';
        cursor.style.fontWeight = '100';
        cursor.style.animation = 'none';
        el.appendChild(cursor);

        const tl = gsap.timeline();
        for (let i = 0; i < text.length; i++) {
            tl.call(() => { cursor.before(text[i]); }, null, i * charDelay);
        }
        // Blink cursor 3 times then remove
        tl.to(cursor, { opacity: 0, duration: 0.3, yoyo: true, repeat: 5, ease: "steps(1)" }, `+=${charDelay * 2}`)
          .call(() => cursor.remove());
    });
};

/**
 * 15. makeMagnetic — CTA buttons, social icons. Element follows cursor elastically.
 * @param {Element} element
 * @param {object} gsap
 * @param {number} power - 35 = soft, 70 = aggressive
 */
export const makeMagnetic = (element, gsap, power = 35) => {
    if (!element) return;
    const xTo = gsap.quickTo(element, "x", { duration: 1, ease: "elastic.out(1, 0.3)" });
    const yTo = gsap.quickTo(element, "y", { duration: 1, ease: "elastic.out(1, 0.3)" });
    element.addEventListener("mousemove", (e) => {
        const rect = element.getBoundingClientRect();
        xTo((e.clientX - (rect.left + rect.width / 2)) * (power / 100));
        yTo((e.clientY - (rect.top + rect.height / 2)) * (power / 100));
    });
    element.addEventListener("mouseleave", () => { xTo(0); yTo(0); });
};

/**
 * 16. hoverUnderline — Navigation links. Underline enters left, exits right.
 * @param {Element} element
 * @param {object} gsap
 */
export const hoverUnderline = (element, gsap) => {
    if (!element) return;
    const line = document.createElement('span');
    Object.assign(line.style, {
        position: 'absolute', bottom: '0', left: '0', width: '100%', height: '1px',
        background: 'currentColor', transformOrigin: 'left center', transform: 'scaleX(0)'
    });
    element.style.position = 'relative';
    element.style.display = 'inline-block';
    element.appendChild(line);
    element.addEventListener("mouseenter", () => {
        gsap.fromTo(line, { scaleX: 0, transformOrigin: "left center" }, { scaleX: 1, duration: 0.4, ease: "power3.inOut" });
    });
    element.addEventListener("mouseleave", () => {
        gsap.to(line, { scaleX: 0, transformOrigin: "right center", duration: 0.4, ease: "power3.inOut" });
    });
};

/**
 * 17. customCursor — Premium agency cursor. Large ring + small dot with lerp delay.
 * @param {object} gsap — Call once per page.
 */
export const customCursor = (gsap) => {
    const ring = document.createElement('div');
    const dot = document.createElement('div');
    const baseRing = { width: '40px', height: '40px', border: '1px solid rgba(255,255,255,0.5)', borderRadius: '50%',
        position: 'fixed', top: '0', left: '0', pointerEvents: 'none', zIndex: '99999', transform: 'translate(-50%,-50%)', mixBlendMode: 'difference' };
    const baseDot = { width: '6px', height: '6px', background: '#fff', borderRadius: '50%',
        position: 'fixed', top: '0', left: '0', pointerEvents: 'none', zIndex: '99999', transform: 'translate(-50%,-50%)' };
    Object.assign(ring.style, baseRing);
    Object.assign(dot.style, baseDot);
    document.body.appendChild(ring);
    document.body.appendChild(dot);

    const pos = { x: 0, y: 0 };
    const ringPos = { x: 0, y: 0 };

    document.addEventListener('mousemove', (e) => {
        pos.x = e.clientX; pos.y = e.clientY;
        gsap.set(dot, { left: pos.x, top: pos.y });
    });

    gsap.ticker.add(() => {
        ringPos.x += (pos.x - ringPos.x) * 0.15;
        ringPos.y += (pos.y - ringPos.y) * 0.15;
        gsap.set(ring, { left: ringPos.x, top: ringPos.y });
    });

    document.querySelectorAll('a, button, [role="button"], .hoverable').forEach(el => {
        el.addEventListener('mouseenter', () => gsap.to(ring, { width: 60, height: 60, borderColor: 'rgba(255,255,255,0.8)', duration: 0.3 }));
        el.addEventListener('mouseleave', () => gsap.to(ring, { width: 40, height: 40, borderColor: 'rgba(255,255,255,0.5)', duration: 0.3 }));
    });
};

/**
 * 18. buttonHover — Primary CTAs. Text slides up, duplicate appears from below (Locomotive-style).
 * @param {Element} element
 * @param {object} gsap
 */
export const buttonHover = (element, gsap) => {
    if (!element) return;
    const text = element.textContent;
    element.innerHTML = '';
    element.style.overflow = 'hidden';
    element.style.position = 'relative';

    const top = document.createElement('span');
    top.textContent = text;
    top.style.display = 'block';
    top.style.transition = 'none';
    const bottom = document.createElement('span');
    bottom.textContent = text;
    Object.assign(bottom.style, { display: 'block', position: 'absolute', top: '100%', left: '0', width: '100%', textAlign: 'center' });
    element.appendChild(top);
    element.appendChild(bottom);

    element.addEventListener("mouseenter", () => {
        gsap.to(top, { yPercent: -100, duration: 0.35, ease: "power2.inOut" });
        gsap.to(bottom, { yPercent: -100, duration: 0.35, ease: "power2.inOut" });
    });
    element.addEventListener("mouseleave", () => {
        gsap.to(top, { yPercent: 0, duration: 0.35, ease: "power2.inOut" });
        gsap.to(bottom, { yPercent: 0, duration: 0.35, ease: "power2.inOut" });
    });
};

/**
 * 19. cardTilt — Pricing/feature cards. 3D tilt following cursor.
 * @param {Element} element
 * @param {number} strength — degrees of tilt (default 8)
 */
export const cardTilt = (element, strength = 8) => {
    if (!element) return;
    element.style.transformStyle = 'preserve-3d';
    element.style.transition = 'transform 0.1s ease-out';
    element.addEventListener('mousemove', (e) => {
        const rect = element.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        element.style.transform = `perspective(1000px) rotateY(${x * strength}deg) rotateX(${-y * strength}deg)`;
    });
    element.addEventListener('mouseleave', () => {
        element.style.transform = 'perspective(1000px) rotateY(0deg) rotateX(0deg)';
    });
};


// ═══════════════════════════════════════════════════════════════════════════
// VI. PAGE TRANSITIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * 20. curtainIn — Page entry. Black overlay slides away revealing content.
 * @param {object} gsap — Call on DOMContentLoaded.
 */
export const curtainIn = (gsap) => {
    const overlay = document.createElement('div');
    Object.assign(overlay.style, {
        position: 'fixed', inset: '0', background: '#000', zIndex: '100000', pointerEvents: 'none'
    });
    document.body.appendChild(overlay);
    gsap.to(overlay, { yPercent: -100, duration: 0.9, ease: "power4.inOut", delay: 0.1, onComplete: () => overlay.remove() });
};

/**
 * 21. curtainOut — Page exit. Black overlay slides up before navigation.
 * @param {string} targetUrl
 * @param {object} gsap
 */
export const curtainOut = (targetUrl, gsap) => {
    const overlay = document.createElement('div');
    Object.assign(overlay.style, {
        position: 'fixed', inset: '0', background: '#000', zIndex: '100000',
        pointerEvents: 'none', transform: 'translateY(100%)'
    });
    document.body.appendChild(overlay);
    gsap.to(overlay, { yPercent: -100, duration: 0.9, ease: "power4.inOut", onComplete: () => { window.location.href = targetUrl; } });
};


// ═══════════════════════════════════════════════════════════════════════════
// QUICK REFERENCE
// ═══════════════════════════════════════════════════════════════════════════
/*
// ─── TEXT ───────────────────────────────────────────────
gsap.effects.wordReveal(".hero-title");
gsap.effects.charReveal(".logo-text", { duration: 0.5 });
gsap.effects.lineReveal(".section-subtitle");
typewriter(".hero-tagline", gsap);
gsap.effects.headingSplit(".split-heading");

// ─── SCROLL REVEALS ─────────────────────────────────────
gsap.effects.revealUp(".section-text");
gsap.effects.revealStagger(".feature-card");
gsap.effects.revealImage(".hero-image");
gsap.effects.revealLine(".divider");

// ─── STATS ──────────────────────────────────────────────
countUp(".stat-number", gsap, { suffix: "%", ScrollTrigger });
gsap.effects.progressBar(".skill-bar", { target: 85 });

// ─── SCROLL MECHANICS ───────────────────────────────────
gsap.effects.parallaxSection(".hero-bg");
gsap.effects.horizontalScroll(".portfolio-track");
gsap.effects.stickyReveal(".features-list");

// ─── UI ─────────────────────────────────────────────────
makeMagnetic(document.querySelector(".cta-btn"), gsap);
hoverUnderline(document.querySelector("nav a"), gsap);
customCursor(gsap);
buttonHover(document.querySelector(".primary-btn"), gsap);
cardTilt(document.querySelector(".pricing-card"));

// ─── TRANSITIONS ────────────────────────────────────────
curtainIn(gsap);
curtainOut("/pricing", gsap);
*/
