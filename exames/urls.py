from django.urls import path
from . import views

app_name = 'exames'

urlpatterns = [
    path('solicitar_exames/', view=views.solicitar_exames, name='solicitar_exames'),
    path('fechar_pedido/', view=views.fechar_pedido, name='fechar_pedido')
]