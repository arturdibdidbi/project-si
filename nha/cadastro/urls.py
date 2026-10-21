from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.cadastro,
        name="cadastro"
    ),

    path(
        "excluir-conta/",
        views.excluir_conta,
        name="excluir_conta"
    ),

]