from django.urls import path
from . import views

app_name = 'exames'

urlpatterns = [
    path('solicitar_exames/', view=views.solicitar_exames, name='solicitar_exames'),
    path('fechar_pedido/', view=views.fechar_pedido, name='fechar_pedido'),
    path('gerenciar_pedidos/', view=views.gerenciar_pedidos, name="gerenciar_pedidos"),
    path("cancelar_pedido/<int:pedido_id>", view=views.cancelar_pedido, name="cancelar_pedido"),
]