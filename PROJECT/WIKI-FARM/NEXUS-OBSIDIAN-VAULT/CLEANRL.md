---
tags: [nexus-vault, ai, reinforcement-learning, cleanrl, pytorch, single-file]
category: AI / Reinforcement Learning (Simplicity)
language: Python
github: https://github.com/vwxyzjn/cleanrl
---

# CLEANRL — High-quality Reinforcement Learning (Single-file)

## Описание
**CleanRL** — это библиотека на **PyTorch** для глубокого обучения с подкреплением (Deep Reinforcement Learning). Но её главная фишка («The Philosophy of CleanRL») в том, что все алгоритмы реализованы **в одном файле** (Single-file implementation). Это позволяет исследователю видеть всё — от подготовки данных до оптимизации градиентов — без прыжков по десяткам подключаемых библиотек.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | PyTorch (v2.0+) |
| Performance | JIT-compilation (TorchJS), Vectorized Envs |
| Algorithms | PPO, DQN, SAC, DreamerV3, PPG |
| Environments | OpenAI Gym / Gymnasium, Atatri, MuJoCo |
| Monitoring | Weights & Biases (W&B), TensorBoard |

## Почему это Killer-App
1. **Understandable**— можно за 15 минут прочитать реализацию SOTA-алгоритма (напр. PPO) сверху вниз.
2. **Reproducible**— в каждом файле указаны точные параметры (Hyperparameters) для получения научных результатов.
3. **Speed**— использование векторизованных окружений позволяет обучать агентов играть в Atari за минуты (на одной GPU).
4. **Library-less**— алгоритмы не зависят от внутренних абстракций библиотеки, они "самодостаточны".

## Архитектурная Ценность для NEXUS
- **Паттерн:** Самообучающиеся Агенты-Пилоты (RL-based Agents). Использование PPO-реализации для обучения NEXUS-дронов [[ARDUPILOT]] в симуляторе [[BULLET3]].
- **Интеграция:** Модуль NEXUS RL-Lab — быстрое создание экспериментальных ИИ-агентов для сложных стратегий (напр. борьба с DDOS).
- **Ключевое:** Использование DreamerV3 (мировой лидер в обучении на основе "образа мира") для долгосрочного планирования.

## Пример запуска (CLI)
```bash
# Обучение агента играть в LunarLander (PPO)
python ppo.py --env LunarLander-v2 --total-timesteps 100000

# Визуализация обучения (W&B)
python ppo.py --track --wandb-project-name nexus_rl
```

## Связанные Репозитории
- [[ALPHAZERO_GOMOKU]] — самообучение в играх
- [[BULLET3]] — самая популярная среда (симулятор) для RL
- [[AUTOGLUON]] — автоматизация обычного МО
- [[CLEAN-CODE-JAVASCRIPT]] — пример того, почему важна чистота кода
- [[DEEP-REINFORCEMENT-LEARNING-ALGORITHMS-WITH-PYTORCH]] — альтернативные реализации
