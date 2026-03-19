# Тестовое задание
Даны модели "Категория Блюд" и "Блюдо" для ресторана и сериализаторы.

Задание: 
- Написать View который вернет для API 127.0.0.1/api/v1/foods/ JSON заданного формата
- В выборку попадают только блюда у которых is_publish=True
- Если в категории нет блюд (или все блюда данной категории имеют is_publish=False) - не включаем ее в выборку
- Запрос в БД сделать любым удобным способом: Django ORM (предпочтительно), Raw SQL, Sqlalchemy…

## Стэк
- Python
- Django REST Framework
- SQLite
- Django ORM
- Docker
- uv (package management)
- flake8, isort

## Установка

```
docker build -t restaurant_test .
docker run -p 8000:8000 restaurant_test
```
После этого будут применены миграции, загружены тестовые данные категорий и блюд, проект будет запущен в dev среде.

## Структура
```
├── Dockerfile  # Конфигурация контейнера для проекта
├── README.md
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings
│   │   ├── base.py  # Базовые настройки проекта
│   │   └── dev.py  # Настройки для разработки
│   ├── urls
│   │   ├── __init__.py
│   │   ├── base.py  # Основные маршруты проекта
│   │   └── dev.py  # Дополнительные маршруты для разработки
│   └── wsgi.py
├── main.py
├── manage.py
├── pyproject.toml
├── restaurant
│   ├── __init__.py
│   ├── fixtures  # тестовые/начальные данные
│   │   ├── categories.csv
│   │   └── foods.csv
│   └── food 
│       ├── __init__.py
│       ├── admin.py  # админка
│       ├── management
│       │   ├── __init__.py
│       │   └── commands
│       │       ├── __init__.py
│       │       └── load_data.py # Команда для загрузки данных из fixtures
│       ├── migrations  # Миграции базы данных
│       ├── models.py  # Определение моделей
│       ├── selectors.py  # Логика БД
│       ├── serializers.py  # Сериализация моделей для API
│       ├── urls.py   # URL маршруты приложения food 
│       └── views.py  # Представления
└── uv.lock
```
## Примечания
- Для загрузки тестовых данных добавлена management command 'load_data'
- Для view  использован `ListAPIView` (возвращает список объектов, автоматически реализует логику чтения данных из базы, их сериализацию, пагинацию)
- Работа с БД вынесена в selectors для разделения ответственности, но без сервисного слоя, так как логика простая
    - selectors → БД
    - view → HTTP
- Добавлен кастомный QuerySet с методами published() и with_additional()
- Проблема  N+1 запросов (для блюд и additional) решена за счет использования prefetch_related, Prefetch, результаты отфильтрованы, отсортированы, без дубликатов. Текущий вариант был выбран поскольку при таком же как и у альтернативы кол-ве выполняемых запросов, он компактен, понятен и более читаем, не переусложнен для текущей задачи.
В качестве альтарнативы рассматривался вариант без join и distinct.
```python
def get_queryset() -> QuerySet[FoodCategory]:
        published_foods = Food.objects.published().with_additional().order_by('code')

        published_foods_subquery = Food.objects.filter(
            category=OuterRef('pk'),
            is_publish=True
        )
        

        qs = FoodCategory.objects.annotate(
                has_published_foods=Exists(published_foods_subquery)
            )
            .filter(has_published_foods=True)
            .prefetch_related(
                Prefetch('food', queryset=published_foods)
            )
            .order_by('order_id', 'id')
        return qs
```
## Возвращаемый JSON

```
    {
        "id": 1,
        "name_ru": "Напитки",
        "name_en": null,
        "name_ch": null,
        "order_id": 10,
        "foods": [
            {
                "internal_code": 100,
                "code": 1,
                "name_ru": "Чай",
                "description_ru": "Чай 100 гр",
                "description_en": null,
                "description_ch": null,
                "is_vegan": false,
                "is_special": false,
                "cost": "123.00",
                "additional": []
            },
            {
                "internal_code": 200,
                "code": 2,
                "name_ru": "Кола",
                "description_ru": "Кола",
                "description_en": null,
                "description_ch": null,
                "is_vegan": false,
                "is_special": false,
                "cost": "123.00",
                "additional": []
            },
            {
                "internal_code": 300,
                "code": 3,
                "name_ru": "Спрайт",
                "description_ru": "Спрайт",
                "description_en": null,
                "description_ch": null,
                "is_vegan": false,
                "is_special": false,
                "cost": "123.00",
                "additional": []
            },
            {
                "internal_code": 400,
                "code": 4,
                "name_ru": "Байкал",
                "description_ru": "Байкал",
                "description_en": null,
                "description_ch": null,
                "is_vegan": false,
                "is_special": false,
                "cost": "123.00",
                "additional": []
            }
        ]
    },
    {
        "id": 2,
        "name_ru": "Выпечка",
        "name_en": null,
        "name_ch": null,
        "order_id": 20,
        "foods": [
            {
                "internal_code": 500,
                "code": 5,
                "name_ru": "Круассан",
                "description_ru": "Свежий круассан",
                "description_en": null,
                "description_ch": null,
                "is_vegan": false,
                "is_special": false,
                "cost": "200.00",
                "additional": []
            }
        ]
    },
    {
        "id": 4,
        "name_ru": "Десерты",
        "name_en": null,
        "name_ch": null,
        "order_id": 40,
        "foods": [
            {
                "internal_code": 900,
                "code": 9,
                "name_ru": "Торт",
                "description_ru": "Шоколадный торт",
                "description_en": null,
                "description_ch": null,
                "is_vegan": false,
                "is_special": false,
                "cost": "500.00",
                "additional": []
            }
        ]
    }
```
