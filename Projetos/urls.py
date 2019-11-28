from django.urls import path
from . import views

app_name = 'Projetos'
urlpatterns = [
    path('', views.Principal, name='principal'),
]