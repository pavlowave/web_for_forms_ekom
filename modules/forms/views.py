from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from modules.forms.models import find_matching_template, validate_field
from modules.forms.serializers import FormInputSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render

class FormMatchingView(APIView):
    @swagger_auto_schema(
        operation_summary='Определение шаблона для введённых данных',
        operation_description=(
            'Проверяет введённые данные и находит подходящий шаблон для их использования. '
            'Если шаблон не найден, возвращает типы полей, определяя их на основе содержимого. '
            'Типы данных могут быть: email, телефон, дата, текст. '
            'Также могут содержаться дополнительные поля.'
            'В случае несоответствия типа данных (например, телефон в поле email), будет возвращена ошибка.'
        ),
        request_body=FormInputSerializer,
        responses={
            200: openapi.Response(
                description='Шаблон найден или типы полей возвращены',
                examples={
                    'application/json': {
                        'template_name': 'Order Form',
                    },
                    'application/json': {
                        'email': 'email',
                        'phone': 'phone',
                        'date': 'date',
                    }
                }
            ),
            400: openapi.Response(
                description='Ошибка валидации данных',
                examples={'application/json': {'error': 'Invalid data'}}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = FormInputSerializer(data=request.data)
        if serializer.is_valid():
            input_fields = serializer.validated_data['fields']
            matching_template = find_matching_template(input_fields)

            if matching_template:
                return Response({"template_name": matching_template}, status=status.HTTP_200_OK)
            else:
                field_types = {field: detect_field_type(value) for field, value in input_fields.items()}
                return Response({
                    "message": "Шаблон не найден, типы полей определены.",
                    "field_types": field_types
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Рендеринг HTML-формы для ввода данных',
        operation_description='Представление формы ввода для сбора данных.',
        responses={
            200: openapi.Response(
                description='Форма для ввода данных',
                examples={'text/html': '<html><body><form>...</form></body></html>'}
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Рендеринг HTML-формы для ввода данных.
        """
        return render(request, 'index.html')
    def get(self, request, *args, **kwargs):
        """
        Рендеринг HTML-формы для ввода данных.
        """
        return render(request, 'index.html')

def detect_field_type(value):
    """
    Функция для определения типа данных на основе значения поля.
    Например, если это email, телефон, дата или обычный текст.
    """
    if validate_field('date', value):
        return 'date'
    elif validate_field('phone', value):
        return 'phone'
    elif validate_field('email', value):
        return 'email'
    return 'text'