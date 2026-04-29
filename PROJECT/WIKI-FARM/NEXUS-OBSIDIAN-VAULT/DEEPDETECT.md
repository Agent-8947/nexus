---
tags: [nexus-vault, ai, inference, machine-learning-as-a-service, deep-learning, c++]
category: AI / Model Deployment (Inference Engine)
language: C++ / Python (Caffe, TensorFlow, PyTorch)
github: https://github.com/jolibrain/deepdetect
---

# DEEPDETECT — Open-Source ML Inference Server (Dedicated)

## Описание
**DeepDetect** — это специализированный **инференс-сервер (Inference Server)** на языке **C++**, разработанный для развертывания моделей машинного обучения в продакшене. Он объединяет в себе поддержку всех основных библиотек (Caffe, TensorFlow, PyTorch, XGBoost, TFLite) и позволяет работать с ними через единый REST API. Это "промышленный" способ превратить любую нейросеть в работающий веб-сервис.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | C++ 14+ (High Performance) |
| Interface | REST/GRPC API (JSON) |
| Backends | PyTorch, TensorFlow, Caffe, XGBoost, ONNX |
| Acceleration | CUDA, TensorRT, OpenVINO, NNPACK |
| Image Ops | OpenCV / FFmpeg (для видео на лету) |

## Почему это Killer-App
1. **Unification**— вам не нужно писать разный код для запуска модели из TensorFlow и из PyTorch. Один API для всего.
2. **Built-in Pre-processing**— Сервер сам умеет менять размер картинок, выделять лица или делать кроп перед сканированием.
3. **Low Latency**— Написание на C++ гарантирует минимальные задержки (overhead) по сравнению с Python-серверами.
4. **Cloud-Native**— Легко упаковывается в Docker и масштабируется в Kubernetes.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Интеллектуальный Сервис-Хаб (AI-as-a-Service Hub). Идеальный "движок" для ваших агентов, когда им нужно распознать объект на фото или классифицировать текст.
- **Интеграция:** Модуль NEXUS Vision API — централизованный сервер, куда все NEXUS-камеры [[CAMERADAR]] шлют кадры для распознавания в реальном времени.
- **Ключевое:** Поддержка инференса на CPU (через OpenVINO), если нет видеокарты.

## Пример вызова (REST API / curl)
```bash
# Создание службы для классификации изображений (ResNet)
curl -X PUT "http://localhost:8080/services/images" -d '{
  "mllib": "caffe",
  "description": "Image classification",
  "type": "supervised",
  "parameters": { "nclasses": 1000 },
  "model": { "repository": "/path/to/models/resnet50" }
}'

# Предсказание по картинке
curl -X POST "http://localhost:8080/predict" -d '{
  "service": "images",
  "parameters": { "output": { "best": 3 } },
  "data": [ "http://url-to-image.jpg" ]
}'
```

## Связанные Репозитории
- [[DEEPLEARNING-500-QUESTIONS]] — теория (чтобы понимать, как это работает)
- [[DATASCIENCEPYTHON]] — подготовка данных (пре-процессинг)
- [[D3]] — визуализация результатов
- [[AIRFLOW]] — планирование запусков инференса
- [[AUTOGLUON]] — автоматическое обучение моделей (которые мы деплоим)
- [[DNA-FARM]] — источник наших данных
- [[DESIGN-PATTERNS]] — архитектурные шаблоны
- [[DEEPSEARCH]] — если нужен поиск по тексту
