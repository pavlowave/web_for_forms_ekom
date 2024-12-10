from rest_framework import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class FormInputSerializer(serializers.Serializer):
    fields = serializers.DictField(
        child=serializers.CharField(),
        help_text="Должен содержать словарь с полями и их значениями. Пример: {'email': 'example@mail.com', 'phone': '+7 999 123 45 67'}. Также могут содержаться дополнительные поля. Пример: {'user_name': 'ExtraUser'} итп."
    )

    @swagger_auto_schema(
        operation_summary='Сериализация данных формы',
        operation_description='Принимает данные формы в виде словаря с полями и их значениями. Используется для сопоставления введённых данных с шаблонами.',
        responses={
            200: openapi.Response(
                description='Данные успешно сериализованы',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'fields': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Словарь с полями и их значениями",
                            additionalProperties=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            400: openapi.Response(
                description='Ошибка валидации данных'
            )
        }
    )
    def validate(self, data):
        """
        Дополнительная валидация данных, если необходимо.
        """
        return data
