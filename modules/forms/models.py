import re
from tinydb import TinyDB
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

db = TinyDB('database/tinydb_database.json')

@swagger_auto_schema(
    operation_summary='Найти подходящий шаблон для данных',
    operation_description='Ищет в базе данных шаблон, который соответствует введённым данным (поля и их типы должны совпадать).',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'input_fields': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='Поля ввода, которые необходимо сопоставить с шаблоном',
                additionalProperties=openapi.Schema(type=openapi.TYPE_STRING)
            )
        },
        required=['input_fields']
    ),
    responses={
        200: openapi.Response(
            description='Шаблон найден',
            examples={
                'application/json': {'template_name': 'template_name_here'}
            }
        ),
        400: openapi.Response(description='Шаблон не найден')
    }
)
def find_matching_template(input_fields):
    """
    Ищет в базе данных шаблон, который соответствует введённым данным.
    """
    templates = db.all()
    for template in templates:
        template_fields = template['fields']
        if all(field in input_fields and validate_field(field_type, input_fields[field])
               for field, field_type in template_fields.items()):
            return template['name']
    return None

@swagger_auto_schema(
    operation_summary='Валидация поля по типу',
    operation_description='Проверяет, соответствует ли значение поля определённому типу (например, дата, телефон, email).',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'field_type': openapi.Schema(type=openapi.TYPE_STRING, description='Тип поля (date, phone, email, text)'),
            'value': openapi.Schema(type=openapi.TYPE_STRING, description='Значение поля для валидации')
        },
        required=['field_type', 'value']
    ),
    responses={
        200: openapi.Response(
            description='Поле валидно',
            examples={'application/json': {'is_valid': True}}
        ),
        400: openapi.Response(description='Ошибка валидации поля')
    }
)
def validate_field(field_type, value):
    """
    Валидация значения поля по его типу.
    """
    if field_type == 'date':
        return re.match(r'^\d{4}-\d{2}-\d{2}$', value) or re.match(r'^\d{2}\.\d{2}\.\d{4}$', value)
    elif field_type == 'phone':
        return re.match(r'^\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$', value)
    elif field_type == 'email':
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value)
    elif field_type == 'text':
        return isinstance(value, str)
    return False
