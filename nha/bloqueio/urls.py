from django.urls import path
from . import views

urlpatterns = [
    path("", views.bloqueio, name="bloqueio"),

    path("criar/", views.criar_bloqueio, name="criar_bloqueio"),

    path("historico/", views.ver_historico, name="historico"),

    path("bloquear/<str:id>/", views.bloquear, name="bloquear"),

    path("desbloquear/<str:id>/", views.desbloquear, name="desbloquear"),
]