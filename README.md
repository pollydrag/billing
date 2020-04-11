### РЕШЕНИЯ:
- aiohttp
- postgres
- sqlalchemy core: к сожалению в данный момент на рынке нет топовой ОРМ для asyncio
- alembic для миграций БД
- jsonschema для валидации реквеста
- pytest + докер в тестах

### ЧТО можно улучшить:
- id-шники не числовые а uuid
- если будет много нагрузки и не не будет удовлетворять SLA избавиться от алхимии
- трансфер вынести в хранимую процедуру
- историю писать триггером
- проверять разные ошибки: повторное создание клиента, существование клиента при пополнение и трансфере

### TODO:
- авторизация в хендлерах (например api-key)

### Requirements
1. Install [Docker](https://www.docker.com/community-edition#/download)
2. Install [Docker Compose](https://docs.docker.com/compose/install/)
3. Install dev packages


### Запуск сервиса
 - Virtualenv

```console
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

 - Зависимости
```console
(venv)$ pip install -r requirements.txt
(venv)$ pip install -r requirements-dev.txt
```

 - БД в докере
```console
$ cd docker
$ docker-compose up -d
```

 - Миграции
```console
(venv)$ alembic upgrade head
```

 - Запуск
```console
PYTHONPATH=. python billing/app.py
```

### Тесты
 - Устанавливаем зависимости и virtualenv
 - запуск тестов
```console
PYTHONPATH=. pytest tests -vv
```
