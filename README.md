# Organizational Structure API

## Технологии
- Python 3.12
- Django 6.0
- DRF-Django Rest Framework
- PostgreSQL
- Docker / Docker Compose

## Запуск

```bash
# Клонировать репозиторий
git clone https://github.com/ваш_логин/org_structure_api.git

# Перейти в папку проекта
cd org_structure_api|cd org_structure_api/.venv ('Если хотите установить зависимости не на глобальном окружении')


# Запустить Docker
docker-compose up -d --build

#Создать и Применить миграции
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate


# Эндпоинты:

GET /departments/ — список отделов

POST /departments/ — создать отдел

GET /departments/{id}/ — отдел + сотрудники + подотделы

POST /departments/{id}/employees/ — создать сотрудника

PATCH /departments/{id}/ — переместить отдел

DELETE /departments/{id}/?mode=cascade/reassign — удалить отдел

#Запуск pytest
docker-compose exec web pytest
```

## API доступно по адресу 
http://localhost:8000/