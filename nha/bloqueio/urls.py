from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.bloqueio,
        name="bloqueio"
    ),

    path(
    "historico/",
    views.ver_historico,
    name="historico"
    ),

]