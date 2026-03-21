---
name: nexus-visual-motion
description: Создание высококачественных веб-анимаций (Luxury/Premium Tier). Включает GSAP для таймлайнов, Lenis для плавного скролла и Threlte для 3D интеграций. Используйте для WOW-эффектов, интерактивных лендингов и микро-взаимодействий.
---

# Nexus Visual Motion & Design Skill

## Overview

Этот навык — точка пересечения кода (GSAP/JS) и профессионального моушн-дизайна (Lottie/Rive). Мы реализуем интерфейсы уровня "Digital Art", где каждое движение обусловлено физикой и смыслом.

## Motion & Design Stack

1. **GSAP 3.12+**: Фундамент для таймлайнов высокого порядка.
2. **Lottie / DotLottie**: Рендеринг векторной графики из After Effects без потери производительности.
3. **Rive**: Сложные интерактивные стейт-машины для микро-взаимодействий.
4. **Physically Based Motion**: Использование инерции, гравитации и веса в анимациях.
5. **Sonic Interface**: Синхронизация визуальных импульсов со звуковыми микро-фидбеками.

## Procedures

### 1. Инициализация GSAP & Lenis

Для создания "жидкого" скролла на странице:

```javascript
import Lenis from '@studio-freight/lenis'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const lenis = new Lenis()
lenis.on('scroll', ScrollTrigger.update)

gsap.ticker.add((time) => {
  lenis.raf(time * 1000)
})
```

### 2. Реализация Reveal-анимаций (Masking)

Используйте `clip-path` и GSAP для премиального появления контента:

```javascript
gsap.from(".hero-text", {
  clipPath: "polygon(0 0, 0 0, 0 100%, 0% 100%)",
  y: 100,
  duration: 1.5,
  ease: "power4.out",
  stagger: 0.2
});
```

### 3. Интеграция 3D (Threlte)

В Svelte-компонентах:

```svelte
<T.PerspectiveCamera makeDefault position={[0, 5, 20]}>
  <OrbitControls enableZoom={false} />
</T.PerspectiveCamera>

<T.DirectionalLight position={[3, 10, 10]} />

<T.Mesh rotation.y={rotation}>
  <T.BoxGeometry args={[5, 5, 5]} />
  <T.MeshStandardMaterial color="#000" metalness={1} roughness={0} />
</T.Mesh>
```

### 4. Интеграция Lottie (Vector Mastery)

```javascript
import lottie from 'lottie-web';

const anim = lottie.loadAnimation({
  container: document.querySelector('#lottie-ui'),
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: 'data.json' // Exported from AE
});
```

### 5. Аудио-Синхронизация (Tactile Response)

```javascript
const triggerImpact = () => {
    // Визуальный импульс
    gsap.to(".ui-card", { scale: 0.98, duration: 0.1, yoyo: true, repeat: 1 });
    // Звуковой отклик
    new Audio('assets/sfx/soft_click.mp3').play();
}
```

## Motion Design Principles (V3.0)

- **Ease-Out Paradigm**: Всегда плавное замедление (`power4.out`). Всплеск энергии в начале, покой в конце.
- **Micro-Delays (Stagger)**: Объекты никогда не двигаются одновременно. Сдвиг в 0.05с создает ощущение "воздуха".
- **Optical Weight**: Более крупные объекты двигаются медленнее и имеют большую инерцию.
- **Secondary Action**: Движение основного объекта вызывает "эхо" или легкое колебание у второстепенных.

## Advanced Shader Mastery (GLSL)

Для визуальных эффектов, невозможных стандартными средствами:

### 1. Custom Shader Integration

Используйте `ShaderMaterial` для процедурных анимаций на GPU:

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uColor: { value: new THREE.Color("#00ffed") }
  },
  vertexShader: `...`,
  fragmentShader: `
    uniform float uTime;
    varying vec2 vUv;
    void main() {
      float pulse = sin(uUv.x * 10.0 + uTime) * 0.5 + 0.5;
      gl_FragColor = vec4(pulse, pulse, pulse, 1.0);
    }
  `
});
```

### 2. Performance Optimization

- **GPU Computing**: Переносите сложную математику в Vertex Shader.
- **Batched Rendering**: Объединение объектов с одинаковым шейдером через `InstancedMesh`.

*Reference Doc*: [ShaderMaterial_Documentation.md](./docs/ShaderMaterial_Documentation.md)

## Best Practices

- **Performance First**: Всегда используйте `will-change: transform` для анимируемых слоев.
- **Subtlety**: Анимация не должна мешать чтению.
- **Aesthetics**: Используйте градиентные свечения (Glow) и размытие (Backdrop Blur) вместе с движением.
