---
description: Запуск NEXUS Motion Engine для создания премиальных веб-анимаций и интерактивных блоков.
---

Этот воркфлоу активирует скилл `nexus-visual-motion` для реализации динамического интерфейса.

### 1. Анализ Сцены (Cortex Phase)

- Определение ключевых объектов для анимации (Hero, Cards, Navigation).
- Выбор типа движения: **Fluid** (Lenis), **Sequence** (GSAP), или **Spatial** (Threlte 3D).

### 2. Сборка Компонента (Assembly)

// turbo
python PROJECT/scripts/motion/generate_motion_module.py

### 3. Применение Скилла

- Интеграция `motion-core.css` для базовых эффектов Reveal и Glow.
- Создание JS-таймлайна для управления критическими кадрами.

### 4. Рендеринг и Просмотр

// turbo
node PROJECT/scripts/motion/build_preview.js

### 5. Валидация

- Проверка производительности (FPS check).
- Проверка адаптивности движения под мобильные устройства.
