---
tags: [nexus-vault, ai, xai, explainability, python]
category: AI / XAI (Explainable AI)
language: Python
github: https://github.com/SeldonIO/alibi
---

# ALIBI — Explainable AI (XAI) Toolkit

## Описание
**Alibi** — библиотека от **Seldon** для интерпретации моделей машинного обучения. Она отвечает на вопрос: **"ПОЧЕМУ черная коробка (нейросеть) выдала именно этот прогноз?"**. Позволяет анализировать как классические модели (scikit-learn), так и глубокое обучение (TF, PyTorch).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.8+ |
| ML Support | scikit-learn, TensorFlow, PyTorch, XGBoost |
| Interpretations | Ale, Anchors, CEM, Counterfactuals |
| SHAP / LIME | Встроенные обертки |

## Ключевые Методы
1. **Accumulated Local Effects (ALE)** — влияние фич на предсказание.
2. **Anchors** — правила, объясняющие исход (сквозные правила "Если А, то Б").
3. **Counterfactuals** — "Что нужно изменить в данных, чтобы получить другой результат?" (например, для отказа в кредите).
4. **Contrastive Explanations Method (CEM)** — что должно присутствовать и что отсутствовать для предсказания.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Доверительный ИИ. Если агент NEXUS ошибается, Alibi находит причину.
- **Интеграция:** Для NEXUS Legal — обоснование отказа или решения (юридическая прозрачность алгоритмов).
- **Ключевое:** Работает с текстом, числами и изображениями.

## Пример: Получение Аналога (Counterfactual)
```python
from alibi.explainers import Counterfactual
# "Что изменить в зарплате и возрасте для одобрения кредита?"
cf = Counterfactual(predict_fn, shape=(1, 10))
explanation = cf.explain(example_input)
print(f"Counterfactual target: {explanation.cf['X']}")
```

## Связанные Репозитории
- [[ALIBI-DETECT]] — обнаружение дрейфа и аномалий
- [[AIF360]] — анализ честности (Bias Aware)
- [[CLEANLAB]] — очистка шумных лейблов
- [[CAUSALML]] — анализ причинности
