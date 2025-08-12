# LDAP Mock Server with FastAPI and OpenLDAP

> Источник OpenLDAP: https://github.com/osixia/docker-openldap

## Обзор

Проект предоставляет полноценную LDAP-среду для разработки и тестирования, включающую:
- 🐳 OpenLDAP сервер в Docker
- 🖥️ Веб-интерфейс phpLDAPadmin
- 🚀 FastAPI для программного управления LDAP

## Архитектура

Сервисы:
1. **openldap** - Основной LDAP сервер (osixia/openldap:1.5.0)
   - Порт: 389 (LDAP), 636 (LDAPS)
   - Домен: example.com
2. **ldap_web_admin** - Веб-интерфейс phpLDAPadmin
   - Порт: 8080
3. **ldap-api** - FastAPI для управления LDAP
   - Порт: 8000
   - Поддерживает CRUD операции через REST

## Быстрый старт

### Требования
- Docker + Docker Compose
- Python 3.10+ (для разработки)

### Запуск
```bash

docker-compose up
```
## Доступ к серверу

## OpenLDAP
- **LDAP**: `ldap://localhost:389`
- **Root DN**: `dc=example,dc=com`
- **Admin**: `cn=admin,dc=example,dc=com`
- **Password**: `admin`

## phpLDAPadmin
- **URL**: [http://localhost:8080](http://localhost:8080)
- **Login**: `cn=admin,dc=example,dc=com`
- **Password**: `admin`

## FastAPI
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **REST API**: [http://localhost:8000](http://localhost:8000)
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
### Изменение записи
```bash

PATCH /entries/cn=testuser3,dc=example,dc=com
Content-Type: application/json

{
   "attributes": {
       "sn": [["MODIFY_REPLACE", ["REPLACED Test User336!!!"]]],
       "telephoneNumber": [["MODIFY_ADD", ["+1234567890"]]]
   }
}
```
### Удаление записи
```bash

DELETE /entries/cn=user1,dc=example,dc=com
```

