---
tags: [nexus-vault, ai, ml, machine-learning, education, python, scikit-learn, pandas, numpy, deep-learning]
category: AI / Machine Learning Education
language: Python, Jupyter Notebook
github: https://github.com/Avik-Jain/100-Days-Of-ML-Code
---

# 100-DAYS-OF-ML-CODE — Практический Курс ML за 100 Дней

## Описание
Структурированный 100-дневный курс машинного обучения с инфографиками, кодом и пошаговыми объяснениями. Покрывает полный ML-цикл: предобработку данных, линейную/логистическую регрессию, SVM, KNN, деревья решений, случайные леса, кластеризацию, нейронные сети, а также математическую базу (линейная алгебра, матанализ). Каждый день — конкретный алгоритм, визуальное объяснение и реализация на Python/Scikit-Learn.

## Основные Разделы
1. **Data Preprocessing** — работа с пропусками, нормализация, кодирование категорий (Days 1–3)
2. **Supervised Learning** — Linear Regression, Logistic Regression, SVM, KNN, Decision Trees, Random Forests (Days 4–34)
3. **Math Foundation** — 3Blue1Brown: Linear Algebra (Days 26–29), Calculus (Days 30–32)
4. **Deep Learning** — Coursera DL Specialization: backprop, CNN, hyperparameter tuning (Days 17–20, 35–42)
5. **Unsupervised Learning** — K-Means Clustering, Hierarchical Clustering (Days 43–54)
6. **Python Data Stack** — NumPy (Days 45–47), Pandas (Days 48–50), Matplotlib (Days 51–53)

## Почему это Killer-App
- **Инфографики** — каждый алгоритм объяснён визуально, не только кодом.
- **Полный стек обучения** — от математической базы до CNN за один связный курс.
- **Scikit-Learn First** — весь код написан с использованием production-ready библиотек, а не велосипедов.
- **26k+ звёзд** — проверено сообществом, используется как вводной курс в тысячах программ.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Готовая обучающая пайплайн-инфраструктура. NEXUS может использовать как шаблон для Data Preprocessing модуля агентов.
- **Интеграция:** Коллекция Scikit-Learn моделей — база для `DNA_AI_Analyzer` агентов в `DNA_12_AST_RENDER`.
- **Ключевое:** Методология "Day-by-Day" применима к структурированию NEXUS Evolution Log — каждая итерация DNA получает свой дневник прогресса.

## Топ-3 примера

```python
# Day 1: Data Preprocessing
from sklearn.preprocessing import StandardScaler, LabelEncoder
sc = StandardScaler()
X_train = sc.fit_transform(X_train)

# Day 14: SVM с kernel trick
from sklearn.svm import SVC
classifier = SVC(kernel='rbf', random_state=0)
classifier.fit(X_train, y_train)

# Day 34: Random Forest
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=10, criterion='entropy')
clf.fit(X_train, y_train)
```

## Связанные Репозитории
- [[100-PANDAS-PUZZLES]] — тренировка pandas для Data Preprocessing
- [[HOMEMADE-MACHINE-LEARNING]] — реализация ML алгоритмов с нуля
- [[SCIKIT-LEARN]] — production библиотека за этим кодом
- [[ML-FROM-SCRATCH]] — альтернативный подход без библиотек
- [[STANFORD-CS-229-MACHINE-LEARNING]] — академическая база
