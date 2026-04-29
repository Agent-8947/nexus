---
tags: [nexus-vault, ai, transformer, forecasting, time-series, python]
category: AI / Forecasting (SOTA)
language: Python
github: https://github.com/thuml/Autoformer
---

# AUTOFORMER — Long-term Time Series Forecasting

## Описание
**Autoformer** — это передовая архитектура нейросети от **Tsinghua University (THU)** для **долгосрочного прогнозирования временных рядов**. Она превосходит классические трансформеры благодаря механизму **Auto-Correlation**, который заменяет стандартный Self-Attention, делая работу с длинными последовательностями в разы эффективнее и точнее.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | PyTorch / Python 3.8+ |
| Architecture | Decomposition-based Transformer |
| Decomposition | Trend-Seasonal (Series Decomposition) |
| Latency | Относительно низкая для глубоких сетей |
| Training | Требует GPU (CUDA) |

## Что внутри (Технология)
1. **Series Decomposition Block** — разделяет входящие данные на "тренд" (долгосрочное изменение) и "сезонность" (регулярные циклы) прямо внутри сети.
2. **Auto-Correlation Mechanism** — находит статистически значимые сходства между фрагментами данных (на разных масштабах времени) и фокусируется на них.
3. **Encoder/Decoder Architecture** — позволяет обучаться на истории и выдавать прогноз на сотни шагов вперед.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Точное планирование будущего (Strategic Forecasting). Намного глубже и точнее, чем простые скользящие средние.
- **Интеграция:** Модуль NEXUS Strategy — прогнозирование экономических показателей, рыночных трендов и нагрузок на сетевую инфраструктуру.
- **Ключевое:** Работает с очень длинными окнами планирования (LSTF).

## Пример запуска (Python)
```python
from models.Autoformer import Model
import torch

# Параметры модели (инкапсулированные в скриптах репозитория)
exp = Exp_Main(args) # Загрузка конфигурации из конфига
exp.train(setting)   # Обучение на специфичных данных (напр. погода, ETTh1)
exp.test(setting)    # Генератор прогноза
```

## Связанные Репозитории
- [[CHRONOS-FORECASTING]] — предобученные модели от Amazon
- [[CAUSALML]] — почему данные меняются
- [[DEEP-LEARNING-TIME-SERIES]] — альтернативные подходы
- [[AUTOGLUON]] — автоматизация обучения других моделей
