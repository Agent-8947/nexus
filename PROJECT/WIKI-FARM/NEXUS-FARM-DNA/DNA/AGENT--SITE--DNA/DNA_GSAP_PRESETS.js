/**
 * NEXUS DNA: GSAP PRESETS ENGINE v2.0
 * Premium Web Animations Library (20 Modern Presets)
 * 
 * Usage:
 * import { initGSAPPresets, makeMagnetic, textReveal } from './DNA_GSAP_PRESETS.js';
 * initGSAPPresets(gsap, ScrollTrigger);
 */

export const initGSAPPresets = (gsap, ScrollTrigger = null) => {

    /* --- 1-5. FADE REVEALS --- */
    gsap.registerEffect({
        name: "fadeUp",
        effect: (targets, config) => gsap.from(targets, { y: config.distance, opacity: 0, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "transform,opacity" }),
        defaults: { duration: 1, distance: 50, ease: "power3.out", stagger: 0 },
        extendTimeline: true
    });

    gsap.registerEffect({
        name: "fadeDown",
        effect: (targets, config) => gsap.from(targets, { y: -config.distance, opacity: 0, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "transform,opacity" }),
        defaults: { duration: 1, distance: 50, ease: "power3.out", stagger: 0 },
        extendTimeline: true
    });

    gsap.registerEffect({
        name: "fadeLeft",
        effect: (targets, config) => gsap.from(targets, { x: config.distance, opacity: 0, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "transform,opacity" }),
        defaults: { duration: 1, distance: 50, ease: "power3.out", stagger: 0 },
        extendTimeline: true
    });

    gsap.registerEffect({
        name: "fadeRight",
        effect: (targets, config) => gsap.from(targets, { x: -config.distance, opacity: 0, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "transform,opacity" }),
        defaults: { duration: 1, distance: 50, ease: "power3.out", stagger: 0 },
        extendTimeline: true
    });

    gsap.registerEffect({
        name: "blurIn",
        effect: (targets, config) => gsap.fromTo(targets, { filter: `blur(${config.amount}px)`, opacity: 0 }, { filter: "blur(0px)", opacity: 1, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "filter,opacity" }),
        defaults: { duration: 1.2, amount: 20, ease: "power2.out", stagger: 0 },
        extendTimeline: true
    });

    /* --- 6-7. SCALING & PHYSICS --- */
    gsap.registerEffect({
        name: "scaleIn",
        effect: (targets, config) => gsap.from(targets, { scale: config.startScale, opacity: 0, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "transform,opacity" }),
        defaults: { duration: 0.8, startScale: 0.8, ease: "back.out(1.5)", stagger: 0 },
        extendTimeline: true
    });

    gsap.registerEffect({
        name: "scaleOut",
        effect: (targets, config) => gsap.to(targets, { scale: config.endScale, opacity: 0, duration: config.duration, ease: config.ease, stagger: config.stagger }),
        defaults: { duration: 0.5, endScale: 0.9, ease: "power2.in", stagger: 0 },
        extendTimeline: true
    });

    /* --- 8-9. CLIP-PATH REVEALS --- */
    gsap.registerEffect({
        name: "clipRevealY",
        effect: (targets, config) => gsap.fromTo(targets, { clipPath: "polygon(0% 100%, 100% 100%, 100% 100%, 0% 100%)", y: config.yOffset }, { clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)", y: 0, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "clipPath,transform" }),
        defaults: { duration: 1.5, yOffset: 40, ease: "power4.inOut", stagger: 0 },
        extendTimeline: true
    });

    gsap.registerEffect({
        name: "clipRevealX",
        effect: (targets, config) => gsap.fromTo(targets, { clipPath: "polygon(0% 0%, 0% 0%, 0% 100%, 0% 100%)", x: config.xOffset }, { clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)", x: 0, duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "clipPath,transform" }),
        defaults: { duration: 1.5, xOffset: -40, ease: "power4.inOut", stagger: 0 },
        extendTimeline: true
    });

    /* --- 10-11. 3D FLIPS --- */
    gsap.registerEffect({
        name: "flipInX",
        effect: (targets, config) => gsap.from(targets, { rotationX: config.angle, opacity: 0, transformPerspective: config.perspective, transformOrigin: "center bottom", duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "all" }),
        defaults: { duration: 1.2, angle: -90, perspective: 1000, ease: "power3.out", stagger: 0 },
        extendTimeline: true
    });

    gsap.registerEffect({
        name: "flipInY",
        effect: (targets, config) => gsap.from(targets, { rotationY: config.angle, opacity: 0, transformPerspective: config.perspective, transformOrigin: "left center", duration: config.duration, ease: config.ease, stagger: config.stagger, clearProps: "all" }),
        defaults: { duration: 1.2, angle: 90, perspective: 1000, ease: "power3.out", stagger: 0 },
        extendTimeline: true
    });

    /* --- 12-14. CONTINUOUS / LOOPS --- */
    gsap.registerEffect({
        name: "float",
        effect: (targets, config) => gsap.to(targets, { y: config.amount, duration: config.duration, ease: "sine.inOut", yoyo: true, repeat: -1 }),
        defaults: { duration: 2, amount: -15 },
        extendTimeline: false
    });

    gsap.registerEffect({
        name: "pulse",
        effect: (targets, config) => gsap.to(targets, { scale: config.scale, duration: config.duration, ease: "sine.inOut", yoyo: true, repeat: -1 }),
        defaults: { duration: 1, scale: 1.05 },
        extendTimeline: false
    });

    gsap.registerEffect({
        name: "glitch",
        effect: (targets, config) => {
            const tl = gsap.timeline({ repeat: config.repeat, yoyo: true });
            tl.to(targets, { x: config.intensity, skewX: 5, duration: 0.05 })
              .to(targets, { x: -config.intensity, skewX: -5, duration: 0.05 })
              .to(targets, { x: 0, skewX: 0, duration: 0.05 });
            return tl;
        },
        defaults: { repeat: 3, intensity: 5 },
        extendTimeline: true
    });

    /* --- 15-17. SCROLLTRIGGER PRESETS --- */
    if (ScrollTrigger) {
        gsap.registerEffect({
            name: "parallax",
            effect: (targets, config) => gsap.to(targets, { y: config.yAmount, ease: "none", scrollTrigger: { trigger: config.trigger || targets, start: "top bottom", end: "bottom top", scrub: config.scrub } }),
            defaults: { yAmount: -100, scrub: true },
            extendTimeline: false
        });

        gsap.registerEffect({
            name: "zoomScrub",
            effect: (targets, config) => gsap.fromTo(targets, { scale: config.startScale }, { scale: 1, ease: "none", scrollTrigger: { trigger: config.trigger || targets, start: "top bottom", end: "center center", scrub: config.scrub } }),
            defaults: { startScale: 0.5, scrub: true },
            extendTimeline: false
        });

        gsap.registerEffect({
            name: "fadeScrub",
            effect: (targets, config) => gsap.fromTo(targets, { opacity: 0, y: config.yOffset }, { opacity: 1, y: 0, ease: "none", scrollTrigger: { trigger: config.trigger || targets, start: "top 90%", end: "center center", scrub: config.scrub } }),
            defaults: { yOffset: 100, scrub: true },
            extendTimeline: false
        });
    }

    /* --- 18. INFINITE MARQUEE --- */
    gsap.registerEffect({
        name: "marquee",
        effect: (targets, config) => gsap.to(targets, { xPercent: -100, ease: "none", duration: config.duration, repeat: -1 }),
        defaults: { duration: 10 },
        extendTimeline: false
    });
};

/* --- 19. MAGNETIC COMPONENT (Function) --- */
export const makeMagnetic = (element, gsap, power = 40) => {
    const xTo = gsap.quickTo(element, "x", { duration: 1, ease: "elastic.out(1, 0.3)" });
    const yTo = gsap.quickTo(element, "y", { duration: 1, ease: "elastic.out(1, 0.3)" });

    element.addEventListener("mousemove", (e) => {
        const rect = element.getBoundingClientRect();
        const relX = e.clientX - (rect.left + rect.width / 2);
        const relY = e.clientY - (rect.top + rect.height / 2);
        xTo(relX * (power / 100));
        yTo(relY * (power / 100));
    });
    element.addEventListener("mouseleave", () => { xTo(0); yTo(0); });
};

/* --- 20. TEXT REVEAL WRAPPER (Function) --- */
/**
 * Splits text into spans (words) without external libraries and animates them.
 */
export const textReveal = (element, gsap, config = {}) => {
    const text = element.innerText;
    element.innerHTML = "";
    
    // Split into words
    const words = text.split(" ");
    const spans = [];
    
    words.forEach(word => {
        const span = document.createElement("span");
        span.style.display = "inline-block";
        span.style.overflow = "hidden";
        span.style.verticalAlign = "top";
        
        const innerSpan = document.createElement("span");
        innerSpan.style.display = "inline-block";
        innerSpan.innerText = word + "\u00A0"; // Add space back
        
        span.appendChild(innerSpan);
        element.appendChild(span);
        spans.push(innerSpan);
    });

    return gsap.from(spans, {
        yPercent: 100,
        opacity: config.fade ? 0 : 1,
        duration: config.duration || 1,
        ease: config.ease || "power4.out",
        stagger: config.stagger || 0.05,
        delay: config.delay || 0
    });
};
