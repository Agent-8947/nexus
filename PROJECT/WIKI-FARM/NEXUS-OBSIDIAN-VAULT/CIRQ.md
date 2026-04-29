---
tags: [nexus-vault, ai, quantum-computing, google, simulation, circuits]
category: AI / Quantum Computing (Sim)
language: Python
github: https://github.com/quantumlib/Cirq
---

# CIRQ — Google Open-Source Framework for NISQ Algorithms

## Описание
**Cirq** — это передовая библиотека на **Python** от **Google Quantum AI Team** для проектирования, симуляции и исполнения квантовых схем (Quantum Circuits) на современных шумных квантовых компьютерах промежуточного масштаба (**NISQ** — Noisy Intermediate-Scale Quantum). Она позволяет писать "квантовый код", который затем можно запустить на реальных процессорах Google (напр. Sycamore).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | Python 3.10+ |
| Backend | QSIM (высокопроизводительный симулятор) |
| Architecture | Qubits, Gates, Circuits, Schedules |
| Target Hardware | Google Sycamore, IonQ, Rigetti (через провайдеры) |
| Integration | TensorFlow Quantum (TFQ) |

## Главные Возможности
1. **Gate Physics** — работа с вентилями (Hadamard, CNOT, Toffoli) на самом низком уровне.
2. **Circuit Simulation** — запуск квантовых программ на обычном CPU (до 20-30 кубитов).
3. **Noisy Simulation** — имитация шума реального квантового процессора для проверки устойчивости алгоритма.
4. **Calibration API** — доступ к данным о "здоровье" и калибровке реального железа.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Будущее Вычислений (Quantum Roadmap). Как решать задачи, невозможные для обычных CPU (напр. взлом сложной криптографии).
- **Интеграция:** Модуль NEXUS Quantum — подготовка и симуляция квантовых алгоритмов оптимизации (QAOA) для логистики.
- **Ключевое:** Использование тензоров для эффективной симуляции квантового состояния.

## Пример кода (Квантовая Схема)
```python
import cirq

# Создаем 2 кубита
q0, q1 = cirq.LineQubit.range(2)
# Создаем квантовую цепь
circuit = cirq.Circuit(
    cirq.H(q0),            # Вентиль Адамара (суперпозиция)
    cirq.CNOT(q0, q1),      # Запутанность (entanglement)
    cirq.measure(q0, q1, key='m') # Измерение
)

# Симуляция на CPU
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=10)
print(result) # (Выдаст список случайных 0 и 1)
```

## Связанные Репозитории
- [[BOTAN]] — классическая криптография (которую "убьют" кванты)
- [[BUILD-YOUR-OWN-X]] — создание своего квантового симулятора
- [[BLACK-HAT-RUST]] — наступательная инженерия
- [[AMARANTH]] — синтез железа на Python
- [[CLOUDQUERY]] — управление инфраструктурой
