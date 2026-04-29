---
tags: [nexus-vault, ai, quantization, llm, gptq, python]
category: AI / Model Optimization
language: Python / C++
github: https://github.com/AutoGPTQ/AutoGPTQ
---

# AUTOGPTQ — 4-bit Post-Training Quantization (PTQ)

## Описание
**AutoGPTQ** — это одна из старейших и наиболее проверенных библиотек для квантования больших моделей (LLM, таких как Llama, Qwen, Mistral). Она основана на алгоритме **GPTQ (Generalized PTQ)**, который позволяет сжимать веса до 4 бит после того, как модель уже обучена (Post-Training). Это стандарт де-факто для высокопроизводительного локального инференса.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | PyTorch / Triton |
| Quantization | 3-bit, 4-bit, 8-bit |
| Format | .safetensors (GPQT variant) |
| Speedup | 2.5x - 4x ускорение токенов в сек. |
| Platform | Linux, Windows (WSL / CUDA) |

## Механика GPTQ
1. **Calibration**— прогон 128-256 примеров текста (например, WikiText) через модель.
2. **Layer-wise Hessian**— расчет "важности" каждого веса через матрицу Гессиана.
3. **Weight Rounding**— округление весов с минимизацией ошибки выходного сигнала каждого слоя.
4. **Kernels**— использование кастомных ядер Triton/CUDA для распаковки 4-битных весов "на лету" прямо в регистрах чипа.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Масштабирование Интеллекта (Intel Scalability). Как запустить Llama-70B на потребительской видеокарте с 24 Гб VRAM (напр. RTX 3090/4090).
- **Интеграция:** Модуль NEXUS Inventory — хранение и автоматическая раздача квантованных моделей агентам.
- **Ключевое:** Самая широкая поддержка моделей среди всех инструментов квантования.

## Пример кода (Python)
```python
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

quantize_config = BaseQuantizeConfig(
    bits=4, group_size=128, damp_percent=0.01, desc_act=False
)

# Загрузка FP16 модели
model = AutoGPTQForCausalLM.from_pretrained("path/to/model", quantize_config)

# Квантование (займет 10-30 мин на 3090)
model.quantize(examples)

# Сохранение (напр. 4 Гб вместо 15 Гб)
model.save_quantized("path/to/quantized_model")
```

## Связанные Репозитории
- [[AUTOAWQ]] — более новый метод (AWQ)
- [[ANYTHING-LLM]] — локальный запуск GPTQ моделей
- [[BREVITAS]] — квантование нейросетей PyTorch
- [[OLLAMA]] — другой формат (GGUF)
