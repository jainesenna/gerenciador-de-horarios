from django.urls import path
from . import views

app_name = 'Projetos'
urlpatterns = [
    path('', views.Principal, name='principal'),
    path('horarios_auto', views.horarios_auto, name='horarios_auto'),
    path('horarios_manual', views.horarios_manual, name='horarios_manual'),
    path('apagar_horarios', views.apagar_horarios, name='apagar_horarios'),
    path('nova_atividade', views.nova_atividade, name='nova_atividade'),
]