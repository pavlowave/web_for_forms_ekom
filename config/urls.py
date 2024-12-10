from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title='Web-приложение для определения заполненных форм',
        default_version='v1',
        description='Documentation `ReDoc` view can be found [here](/redoc).',
        contact=openapi.Contact(email='pavlosidorov@mail.ru'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('modules.forms.urls')),
]
