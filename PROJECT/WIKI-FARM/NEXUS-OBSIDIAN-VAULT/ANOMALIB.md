---
tags: [nexus-vault, ai, anomaly-detection, computer-vision, deep-learning, python]
category: AI / Computer Vision
language: Python
github: https://github.com/openvinotoolkit/anomalib
---

# ANOMALIB — Deep Learning Anomaly Detection Library

## Описание
**Anomalib** — это современная библиотека (библиотека-флагман от Intel/OpenVINO) для **обнаружения аномалий в изображениях и видео**. Она предназначена для задач контроля качества на производстве (поиск дефектов), медицинского анализа и видеомониторинга (поиск странного поведения).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | PyTorch / PyTorch Lightning |
| Acceleration | OpenVINO, ONNX, TensorRT |
| Algorithms | PatchCore, PaDiM, FastFlow, Draem |
| Metrics | AUROC, F1, Pixel-level segmentation |
| Datasets | MVTec AD, Bean, custom importers |

## Ключевые Методы
1. **Reconstruction-based** — нейросеть учится "нормальному" виду объекта; аномалия — то, что она не может восстановить.
2. **Embedding-based** — сравнение признаков (embeddings) "нормального" и "текущего" объекта в многомерном пространстве.
3. **PatchCore** — одно из самых точных решений: сохранение "библиотеки" кусочков (патчей) нормальных объектов.
4. **Segmentation** — отрисовка точной маски дефекта на картинке.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Автоматический контроль качества визуальных данных. "Это фото — подделка (Deepfake) или оригинал?"
- **Интеграция:** Модуль NEXUS Vision — обнаружение посторонних лиц, предметов или подозрительной активности на видеопотоках (через [[CAMERADAR]]).
- **Ключевое:** Использование OpenVINO для сверхбыстрого инференса на обычных процессорах CPU.

## Пример Конфигурации (YAML)
```yaml
dataset:
  name: mvtec
  category: bottle
  image_size: [256, 256]

model:
  name: patchcore
  backbone: wide_resnet50_2
  layers: [layer2, layer3]

threshold:
  method: adaptive
```

## Связанные Репозитории
- [[ALIBI-DETECT]] — аномалии в обычных данных (не-видео)
- [[CELLPOSE]] — анализ клеток на фото
- [[COMPUTERVISION-RECIPES]] — шаблоны для компьютерного зрения
- [[AUTOGLUON]] — автоматизация обучения
