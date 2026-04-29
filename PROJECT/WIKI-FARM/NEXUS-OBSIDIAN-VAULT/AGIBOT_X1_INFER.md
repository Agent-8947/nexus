---
tags: [nexus-vault, robotics, humanoid, agibot, inference, aimrt, reinforcement-learning, ros2, computer-vision, cplusplus]
category: AI / Robotics Control
language: C++, Python
github: https://github.com/agibot/AGIBOT_X1_INFER
---

# AGIBOT X1 INFER — Среда Инференса для Модульного Гуманоида

## Описание
Программное обеспечение для автономного гуманоидного робота **AgiBot X1**. Репозиторий включает модули инференса моделей (Reinforcement Learning), драйверы платформы и средства симуляции. Система построена на базе промежуточного ПО `AimRT` (AgiBot's open-source framework) и оптимизирована для управления движением (locomotion control) в реальном времени.

## Основные Разделы
1. **Model Inference** — запуск обученных RL-политик через ONNX Runtime.
2. **Platform Driver** — низкоуровневое управление приводами и сенсорами робота.
3. **Software Simulation** — интеграция с ROS2 Humble и MuJoCo для отладки "в цифре".
4. **AimRT Middleware** — масштабируемая архитектура обмена сообщениями между модулями.
5. **Joystick Control** — модуль ручного управления и калибровки через Logitech F710.

## Почему это Killer-App
- **Sim-to-Real** — готовая инфраструктура для переноса обученных в симуляции навыков на реальное железо.
- **Embedded Performance** — использование C++ 13 и ONNX Runtime для минимальной задержки (latency) управления.
- **Modular Hardware Support** — поддержка модульной конструкции робота (различные конфигурации DOF).
- **Real-Time Ready** — поддержка патчей реального времени (RT kernel) для Linux.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Humanoid Core — эталонная архитектура для NEXUS Robotics агентов.
- **Интеграция:** Использование `AimRT` как альтернативы ROS2 для более легких и быстрых агентских коммуникаций.
- **Ключевое:** Протоколы обмена данными (`src/protocols`) могут быть адаптированы для меж-агентского взаимодействия в NEXUS.

## Топ-3 технических фишки
- **ONNX Runtime Support:** Универсальный запуск моделей, обученных в PyTorch/TensorFlow.
- **AimRT Integration:** Высокопроизводительная шина данных, разработанная специально для роботов.
- **Joystick Mapping:** Продвинутая логика интерпретации команд оператора в 3D-движения.

## Связанные Репозитории
- [[AIMRT]] — базовый фреймворк
- [[AGIBOT_X1_TRAIN]] — код для обучения этого робота
- [[ROS2]] — среда симуляции и вспомогательные инструменты
- [[MUJOCO]] — физический движок
