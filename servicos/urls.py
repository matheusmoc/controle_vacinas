from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_servico, name="listar_servico"),
    path('novo_servico/', views.novo_servico, name="novo_servico"),
    path('servico/<str:identificador>', views.servico, name="servico"),
    path('gerar_carteira_vacinacao/<str:identificador>', views.gerar_carteira_vacinacao, name='gerar_carteira_vacinacao')
]
