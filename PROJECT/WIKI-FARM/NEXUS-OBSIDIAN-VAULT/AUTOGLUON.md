---
tags: [nexus-vault, ai, automation, automl, machine-learning]
category: AI / Auto-ML
language: Python
github: https://github.com/autogluon/autogluon
---

# AUTOGLUON — Automated Machine Learning (AutoML)

## Описание
**AutoGluon** — библиотека от **AWS**, которая позволяет обучать сверхточные модели для табличных данных, текста и изображений всего **тремя строками кода**. Она автоматически выбирает лучшие алгоритмы (XGBoost, CatBoost, NN, LightGBM) и ансамблирует их для достижения максимальной точности.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.8+ |
| ML Engines | PyTorch, MXNet, Scikit-learn, XGBoost |
| Hyperparameters | Bayesian Optimization (Ray Tune / BoTorch) |
| Ensemble | Stacked Ensemble / Multi-layer Stacking |

## Ключевое Преимущество
- **Tabular Data Mastery**— лучшая в мире модель для "табличек" (CSV/Excel).
- **Multi-modal Support**— может одновременно учиться на тексте, цифрах и картинках в одной таблице.
- **Deep Stacking**— строит иерархию моделей (одни модели учатся на ошибках других).
- **Time-limit Aware**— скажи ей: "У тебя 1 час", и она выдаст лучший результат за это время.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Автономное обучение без Data Scientist-а. Агент может сам обучить модель на собранных данных.
- **Интеграция:** Идеально для NEXUS Legal Module (классификация документов) и NEXUS Security (классификация атак).
- **Ключевое:** Не нужно настраивать гиперпараметры — всё делается "под капотом".

## Пример кода (Tabular)
```python
from autogluon.tabular import TabularPredictor

# Обучение на "грязных" данных
predictor = TabularPredictor(label='target').fit(train_data)

# Прогноз за секунду
predictions = predictor.predict(test_data)
# Оценка качества (Leaderboard)
print(predictor.leaderboard(test_data))
```

## Связанные Репозитории
- [[AIF360]] — аудит моделей на честность (Bias)
- [[CLEANLAB]] — очистка шумных лейблов в данных
- [[CHRONOS-FORECASTING]] — прогнозы временных рядов
- [[CAUSALML]] — анализ причинно-следственных связей
- [[DATA-JUICER]] — подготовка данных (пре-процессинг)
