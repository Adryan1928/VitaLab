from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path(route='cadastro/', view=views.cadastro, name='cadastro'),
    path(route='login/', view=views.logar, name='login')
]