# Сравнение производительности REST и gRPC API

Нагрузочное тестирование приложения-глоссария блокчейн терминов с использованием Locust.

## Описание проекта

Сравнительный анализ производительности двух реализаций API:
- **REST API** (FastAPI + JSON)
- **gRPC API** (FastAPI + Protocol Buffers)

## Технологии

- **Backend**: FastAPI
- **Database**: Neo4j (графовая БД)
- **Load Testing**: Locust 2.43.1
- **Protocols**: HTTP/1.1 + JSON, HTTP/2 + Protobuf

## Структура репозитория
```
.
├── locust_tests/
│   ├── rest_locustfile.py      # Тесты для REST API
│   └── grpc_locustfile.py      # Тесты для gRPC API
├── results/
│   ├── rest_light.html         # Результаты легкой нагрузки REST
│   ├── grpc_light.html         # Результаты легкой нагрузки gRPC
│   ├── rest_normal.html        # Результаты рабочей нагрузки REST
│   ├── grpc_normal.html        # Результаты рабочей нагрузки gRPC
│   ├── rest_stability.html     # Результаты теста стабильности REST
│   ├── grpc_stability.html     # Результаты теста стабильности gRPC
│   ├── rest_stress.html        # Результаты стресс-теста REST
│   └── grpc_stress.html        # Результаты стресс-теста gRPC
├── README.md                   # Этот файл
└── REPORT.md                   # Полный отчет по тестированию
```

## Быстрый старт

### Требования

- Python 3.11+
- Locust 2.43.1+

### Установка
```bash
pip install locust grpcio grpcio-tools
```

### Запуск тестов

#### Легкая нагрузка (10 users)
```bash
locust -f locust_tests/rest_locustfile.py --headless -u 10 -r 1 -t 30s --html results/rest_light.html
locust -f locust_tests/grpc_locustfile.py --headless -u 10 -r 1 -t 30s --html results/grpc_light.html
```

#### Рабочая нагрузка (50 users)
```bash
locust -f locust_tests/rest_locustfile.py --headless -u 50 -r 5 -t 60s --html results/rest_normal.html
locust -f locust_tests/grpc_locustfile.py --headless -u 50 -r 5 -t 60s --html results/grpc_normal.html
```

#### Тест на стабильность (50 users, 120s)
```bash
locust -f locust_tests/rest_locustfile.py --headless -u 50 -r 5 -t 120s --html results/rest_stability.html
locust -f locust_tests/grpc_locustfile.py --headless -u 50 -r 5 -t 120s --html results/grpc_stability.html
```

#### Стресс-тест (100 users)
```bash
locust -f locust_tests/rest_locustfile.py --headless -u 100 -r 10 -t 60s --html results/rest_stress.html
locust -f locust_tests/grpc_locustfile.py --headless -u 100 -r 10 -t 60s --html results/grpc_stress.html
```

## Ключевые результаты

### Сравнение производительности

| Сценарий | REST RPS | gRPC RPS | Победитель |
|----------|----------|----------|------------|
| Light (10u) | 4.32 | 4.51 | gRPC |
| Normal (50u) | 21.21 | 7.97 | REST (2.7x) |
| Stability (50u, 120s) | 22.11 | 7.47 | REST (3.0x) |
| Stress (100u) | 42.74 | 5.27 | REST (8.1x) |

### Основные выводы

- REST показывает превосходную масштабируемость под нагрузкой (в 3-8 раз выше RPS)
- gRPC лучше при легкой нагрузке (<10 users) с минимальной латентностью
- Оба протокола: 0% ошибок во всех сценариях
- gRPC деградирует при 50+ одновременных пользователях

### Рекомендации

**Использовать REST для:**
- Высоконагруженных систем (50+ RPS)
- Публичных API
- Непредсказуемых нагрузок

**Использовать gRPC для:**
- Внутренних микросервисов с низкой нагрузкой
- Критичной минимальной латентности
- Потоковой передачи данных
