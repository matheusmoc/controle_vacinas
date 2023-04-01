from django.urls import path
from . import views

urlpatterns = [
    path('', views.pacientes, name="pacientes"),
    path('/atualiza_paciente/',  views.att_paciente, name="atualiza_paciente")
]
