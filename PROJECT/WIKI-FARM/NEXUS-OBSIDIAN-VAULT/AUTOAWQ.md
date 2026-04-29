---
tags: [nexus-vault, ai, quantization, llm, cuda, ml]
category: AI / Model Optimization
language: Python / C++ / CUDA
github: https://github.com/casper-hansen/AutoAWQ
---

# AUTOAWQ — 4-bit Quantization (AWQ) for Large Models

## Описание
**AutoAWQ** — это передовая библиотека для **квантования весов (Weight Quantization)** больших языковых моделей (LLM, таких как Llama-3, Mixtral) до 4 бит. В ней используется алгоритм **AWQ (Activation-aware Weight Quantization)**, который обеспечивает в 3 раза меньший объем памяти при почти нулевой потере качества.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | PyTorch / CUDA |
| Quantization | 4-bit Group-wise (W4A16) |
| Kernels | ExLlamaV2, Marlin |
| Target GPU | NVIDIA (Ampere, Hopper, Ada) |
| Speed | До 2-3x быстрее, чем FP16 |

## Порядок Работы (AWQ)
1. **Calibration** — модель прогоняет небольшую часть данных («калибровка»).
2. **Weight Protection** — алгоритм находит **самые важные веса** (на основе активаций) и оставляет их в высоком качестве, квантуя остальные.
3. **Save** — результат сохраняется в `.safetensors`.
4. **Deploy** — модель весом 70 Гб теперь весит 18 Гб и работает на домашней видеокарте.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Экономика ресурсов (VRAM Economics). Как запустить мощный ИИ в локальном NEXUS "подвале".
- **Интеграция:** Модуль NEXUS Deployer — автоматическое квантование новых моделей перед их использованием агентами.
- **Ключевое:** Использование ядра Marlin для сверхскоростного вывода (инференса).

## Пример Квантования (Python)
```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = "meta-llama/Llama-3-8b"
quant_path = "Llama-3-8b-awq"
quant_config = { "zero_point": True, "q_group_size": 128, "w_bit": 4, "version": "GEMM" }

# Загрузка и квантование
model = AutoAWQForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.quantize(tokenizer, quant_config=quant_config)

# Сохранение квантованной модели
model.save_quantized(quant_path)
```

## Связанные Репозитории
- [[AUTOGPTQ]] — альтернативный метод квантования (GPTQ)
- [[ANYTHING-LLM]] — локальный запуск таких моделей
- [[OLLAMA]] — GGUF формат (другая ветка оптимизации)
- [[CHARTGPU]] — визуализация нагрузки на GPU
