from django.urls import path
from .views import confirmar_presenca, confirmacao_sucesso, lista_convidados

urlpatterns = [
    path('', confirmar_presenca, name='confirmar_presenca'),
    path('sucesso/', confirmacao_sucesso, name='confirmacao_sucesso'),
    path('convidados/', lista_convidados, name='lista_convidados'),
]
