# 🎬 Printivo Video Production Pipeline

Этот воркфлоу запускает S-Tier синтез маркетинговых видео-комплектов для Printivo.

## 🛠 Подготовка
- [ ] Убедиться, что в `INDEX.html` кейса есть `window.mainTimeline = ...`
- [ ] Проверить наличие установленного Python и Playwright

## 🚀 Запуск синтеза
// turbo
```powershell
# Запуск визуального рендеринга для конкретного кейса (по умолчанию 65)
# Форматы: 16:9, 9:16, 3:4
python "E:\Downloads\--Agent V\MOTION-synt\VISUAL_FORGE.py" 65
```

## 📋 Параметры (VISUAL_FORGE.py)
Вы можете запустить рендер для любого кейса, передав номер аргументом:
- `python VISUAL_FORGE.py 63` — Геометрический синтез
- `python VISUAL_FORGE.py 64` — Chroma Vortex
- `python VISUAL_FORGE.py 65` — Swiss Layout Synth

## 📦 Результаты
После завершения файлы будут доступны в папке `SNAPSHOTS` соответствующего кейса:
- `*_FORGE_16_9.webm`
- `*_FORGE_9_16.webm`
- `*_FORGE_3_4.webm`

> [!IMPORTANT]
> Рендеринг происходит в **видимом окне**. Пожалуйста, не закрывайте окно браузера до завершения захвата всех кадров.
