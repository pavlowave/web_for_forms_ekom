from django.urls import path
from django.contrib.auth import views as auth_views
from modules.forms.views import FormMatchingView


urlpatterns = [
    path('get_form/', FormMatchingView.as_view(), name='get_form'),
]