from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "cadastro/",
        include("cadastro.urls")
    ),

    path(
        "login/",
        include("login.urls")
    ),

    path(
        "objetivos/",
        include("objetivos.urls")
    ),

    path(
            "bloqueio/",
            include("bloqueio.urls")
        ),

   

    path(
        "bloqueio/",
        include("bloqueio.urls")
    ),


]