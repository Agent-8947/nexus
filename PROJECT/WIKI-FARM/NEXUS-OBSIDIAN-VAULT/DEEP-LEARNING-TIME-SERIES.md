---
tags: [nexus-vault, ai, transformer, forecast, series, time-series, python]
category: AI / Forecasting (Advanced Time Series)
language: Python
github: https://github.com/thuml/Informer2020 (Informer, Autoformer, FEDformer)
---

# DEEP-LEARNING-TIME-SERIES — SOTA Transformers for Forecasting

## Описание
Этот репозиторий (часто связываемый с легендарной статьей по **Informer** и **Autoformer**) представляет собой коллекцию передовых архитектур нейросетей для **долгосрочного прогнозирования временных рядов (LSTF)**. Основная проблема классических Трансформеров — они "дышат тяжело" на длинных последовательностях (сложность $O(L^2)$). Здесь эта проблема решена через **ProbSparse Attention** и другие оптимизации, позволяя моделировать зависимости на тысячи шагов вперед.

## Ключевые Архитектуры
1. **Informer (SOTA 2021)**— Внедрение ProbSparse Self-attention, который уменьшает сложность до $O(L \log L)$, позволяя работать с экстремально длинными окнами.
2. **Autoformer (SOTA 2022)**— Иерархическое разложение временного ряда (Series Decomposition) прямо внутри слоев Трансформера (Trend + Seasonal).
3. **FEDformer (SOTA 2023)**— Использование преобразования Фурье и вейвлетов (Frequency Domain) для понимания циклических и долгосрочных паттернов.
4. **PatchTST (SOTA 2024)**— Разбиение ряда на патчи (как в Vision Transformer), что повышает точность и снижает шум.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Language | Python 3.8+ / PyTorch |
| Accelerator | CUDA (High VRAM usage recommended) |
| Layout | Encoder-only / Encoder-Decoder |
| Datasets | ETTh1/2, Electricity, Weather, Exchange, Nexus Traffic |
| Metrics | MSE (Mean Squared Error), MAE |

## Архитектурная Ценность для NEXUS
- **Паттерн:** Сверхточное Планирование Будущего (Predictive Foresight). Идеально для предсказания нагрузки на серверы, цен на активы или "волн" юридических запросов.
- **Интеграция:** Модуль NEXUS Oracle — прогнозирование будущих уязвимостей на основе исторических данных сканирований.
- **Ключевое:** Работает с многомерными данными (Multivariate), учитывая взаимосвязи между разными показателями (напр. "Цена" и "Объем").

## Пример запуска (Python/CLI)
```bash
# Запуск обучения Informer на датасете Electricity
python -u main_informer.py --model informer --data custom --features M --seq_len 96 --label_len 48 --pred_len 24

# Результаты: Предсказание на 24 шага вперед на основе 96 прошлых шагов
```

## Связанные Репозитории
- [[CHRONOS-FORECASTING]] — готовые модели от Amazon (из этого класса)
- [[AUTOFORMER.md]] — выделенная страница по одной из моделей
- [[CAUSALML]] — почему данные меняются
- [[DEEPLEARNING-500-QUESTIONS]] — теория (глава по временным рядам)
- [[DATASCIENCEPYTHON]] — подготовка данных (пре-процессинг)
- [[D3]] — визуализация прогнозов
- [[AIRFLOW]] — планирование запусков обучения
- [[DNA-FARM]] — источник наших данных
- [[DESIGN-PATTERNS]] — архитектурные шаблоны
