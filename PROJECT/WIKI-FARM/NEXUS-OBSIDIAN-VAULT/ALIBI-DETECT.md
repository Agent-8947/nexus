---
tags: [nexus-vault, ai, monitoring, anomaly-detection, outlier]
category: AI / Monitoring (Data Drift)
language: Python
github: https://github.com/SeldonIO/alibi-detect
---

# ALIBI-DETECT — Drift & Anomaly Detection

## Описание
Брат-близнец ALIBI, но сфокусированный на **мониторинге данных в реальном времени**. Обнаруживает аномалии, выбросы (outliers) и дрейф данных (когда модель начинает ошибаться, потому что мир изменился).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.8+ |
| Backend | PyTorch, TensorFlow |
| Metrics | Kolmogorov-Smirnov, MMD, Chi-Squared |
| Drifts | Covariate Drift, Label Drift |
| Anomaly | VAE, Isolation Forest, Mahalanobis |

## Ключевые Возможности
1. **Outlier Detection** — поиск редких событий (фрод, сбой датчика).
2. **Data Drift Detection** — сравнение входящего потока данных с эталоном.
3. **Adversarial Detection** — обнаружение атак на МО (враждебных примеров).
4. **Online Monitoring** — скользящие окна для анализа потоковых данных.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Система раннего предупреждения. "Поток данных от агентов изменился!" (Началась атака или сбой).
- **Интеграция:** Модуль NEXUS Monitor — автоматическая проверка качества данных в реальном времени.
- **Ключевое:** Работает с картинками (через VAE) и текстом (через эмбеддинги).

## Пример: Ошибка Дрейфа (Drift Detection)
```python
from alibi_detect.cd import KSDrift
cd = KSDrift(X_ref, p_val=.05)
preds = cd.predict(X_test)
print(f"Drift detected: {preds['data']['is_drift']}")
```

## Связанные Репозитории
- [[ALIBI]] — интерпретируемость моделей
- [[AIF360]] — анализ честности
- [[CLEANLAB]] — очистка шумных лейблов
- [[CHRONOS-FORECASTING]] — прогнозы временных рядов
