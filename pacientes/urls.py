from django.urls import path
from . import views

urlpatterns = [
    path('', views.pacientes, name="pacientes"),
    path('atualiza_paciente/',  views.att_paciente, name="atualiza_paciente"),
    path('excluir_vacina/<int:id>', views.excluir_vacina, name="excluir_vacina"),
    path('update_vacina/<int:id>', views.update_vacina, name="update_vacina"),
    path('update_paciente/<int:id>', views.update_paciente, name="update_paciente"),
]
