---
tags: [nexus-vault, ai, robotics, reinforcement-learning, isaac-gym, humanoid, pytorch, sim-to-real, locomotion, training]
category: AI / Robotics Training
language: Python
github: https://github.com/agibot/AGIBOT_X1_TRAIN
---

# AGIBOT X1 TRAIN — Система Обучения с Подкреплением для Гуманоидов

## Описание
Специализированная среда для обучения гуманоидных роботов (AgiBot X1) навыкам ходьбы и балансировки с использованием Reinforcement Learning. Система базируется на Isaac Gym (NVIDIA), что позволяет симулировать тысячи роботов параллельно на GPU. Репозиторий предоставляет полный цикл: от настройки URDF-модели робота до экспорта готовых JIT/ONNX весов для реального инференса.

## Основные Разделы
1. **Env Directory** — определение конфигураций среды (LeggedRobotCfg) и логики вознаграждений.
2. **Algo Directory** — реализация RL алгоритмов (на базе PPO/RSL_RL).
3. **Sim2Sim Validation** — проверка обученных политик в MuJoCo перед деплоем на робота.
4. **Export Tools** — скрипты для генерации JIT-моделей (TorchScript) и ONNX.
5. **Resources** — библиотека мешей, URDF и MJCF файлов робота AgiBot X1.

## Почему это Killer-App
- **Massive Parallelism** — обучение сложной локомоции за часы вместо недель благодаря Isaac Gym.
- **Zero-Shot Transfer** — оптимизация под Sim-to-Real перенос (обучение робастности в симуляции).
- **Extensibility** — легкое добавление новых роботов через наследование базовых классов `LeggedRobot`.
- **Comprehensive Benchmarks** — включает задачи `x1_dh_stand` и другие фундаментальные навыки.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Agentic Learning Factory — NEXUS может использовать этот подход для обучения цифровых агентов сложным операциям в "виртуальных песочницах".
- **Интеграция:** Принципы настройки вознаграждений (Reward function) применимы для фитнес-функций в NEXUS DNA.
- **Ключевое:** Использование `sim2sim.py` для adversarial-тестирования стратегий поведения.

## Рабочий цикл обучения (NEXUS focus)
1. **Train:** `python scripts/train.py --task=x1_dh_stand --headless`
2. **Play:** Визуальная оценка обученной политики в Isaac Gym.
3. **Export:** Генерация ONNX модели для `AGIBOT_X1_INFER`.
4. **Verify:** Финальный тест в MuJoCo (`scripts/sim2sim.py`).

## Связанные Репозитории
- [[ISAACGYM]] — фундамент от NVIDIA
- [[RSL_RL]] — быстрая реализация RL алгоритмов на GPU
- [[HUMANOID-GYM]] — идейный предшественник
- [[MUJOCO]] — проверочная симуляция
