from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
            "editlogin/",
            views.editLogin_view,
            name="editlogin"
        ),

    path(
                "check/",
                views.Check_view,
                name="check"
            ),
    path(
                "change/",
                views.Change_view,
                name="change"
            ),
]