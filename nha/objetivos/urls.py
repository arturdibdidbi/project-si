from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.inicio,
        name="inicio"
    ),

    path(
        "criar/",
        views.criar_objetivo,
        name="criar_objetivo"
    ),

    path(
        "<str:objetivo_id>/",
        views.objetivo,
        name="objetivo"
    ),

    path(
        "<str:objetivo_id>/marco/",
        views.criar_marco,
        name="criar_marco"
    ),

    path(
        "<str:objetivo_id>/tarefa/",
        views.criar_tarefa,
        name="criar_tarefa"
    ),

    path(
        "tarefa/<str:tarefa_id>/concluir/",
        views.concluir_tarefa,
        name="concluir_tarefa"
    ),

    path(
        "tarefa/<str:tarefa_id>/excluir/",
        views.excluir_tarefa,
        name="excluir_tarefa"
    ),

    path(
        "<str:objetivo_id>/excluir/",
        views.excluir_objetivo,
        name="excluir_objetivo"
    ),

    path(
        "graficos/",
        views.graficos,
        name="graficos"
    ),
]