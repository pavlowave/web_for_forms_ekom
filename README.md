<h1 align="center">Web-приложение для определения заполненных форм</h1>

<div align="center">

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django Rest Framework](https://img.shields.io/badge/django_rest_framework-0C4B33?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![TinyDB](https://img.shields.io/badge/tinydb-%234CAF50.svg?style=for-the-badge&logo=tinydb&logoColor=white)](https://tinydb.readthedocs.io/)


</div>

Выполнено в рамках [тестового задания](https://app.affine.pro/workspace/f6dfe706-59c0-41e5-898b-9d6a25d84efe/F20QnCRuwfcgPkZeQb9UH)

## Установка и запуск:

1. Склонируйте репозиторий и еперйдите в папку

```
git clone https://github.com/pavlowave/web_for_forms_ekom
cd web_for_forms_ekom
```

2. В корневой папке проекта создайте и заполните файл .env:

```
DEBUG=True
SECRET_KEY='i_22eto6s8g+&c8)nyyfa9e_7(l==(sfbvm7+q9d=bd#jv!q5'
```

3. Запустите проект c помощью Docker:

```
docker-compose up --build
```

4. Приложение будет доступно по адресу http://127.0.0.1:8000/get_form/

## Использование

Документация API доступна по адресу:

- http://127.0.0.1:8000/redoc/ (Redoc)
- http://127.0.0.1:8000/swagger/ (Swagger)
