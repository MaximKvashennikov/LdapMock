# LDAP Mock Server с FastAPI
> Источник: https://github.com/osixia/docker-openldap


## Обзор

Проект предоставляет мок-сервер LDAP с REST API для управления, упакованный в Docker. Используется для тестирования приложений, работающих с LDAP, без реального сервера.

## Возможности

- 🚀 Эмуляция LDAP через `ldap3.MOCK_SYNC`
- 📡 Управление через REST API (CRUD операции)
- 🐳 Готовая Docker-сборка
- 🔄 Поддержка Python 3.10+
- 📊 Импорт/экспорт данных в JSON

## Быстрый старт

### Требования
- Docker + Docker Compose
- Python 3.10+ (для разработки)

### Запуск
```bash

docker-compose up --build
```

## Доступ к серверу

Сервер будет доступен на порту **8000**:  
[http://localhost:8000/docs](http://localhost:8389/docs) (Swagger UI)

## Использование API

### Добавление записи
```bash

POST /entries/
Content-Type: application/json

{
  "dn": "cn=user1,dc=example,dc=com",
  "attributes": {
    "objectClass": ["person"],
    "cn": "user1",
    "sn": "Test User"
  }
}
```
### Поиск записи
```bash

GET /entries/?base_dn=dc=example,dc=com
```

### Удаление записи
```bash

DELETE /entries/cn=user1,dc=example,dc=com
```

