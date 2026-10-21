from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, PassEdit, CodeInput, ChangePass
from cadastro.mongo import usuarios


def login_view(request):

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]

            usuario = usuarios.find_one({
                "email": email
            })

            if usuario and check_password(
                senha,
                usuario["senha"]
            ):

                request.session["usuario_id"] = str(
                    usuario["_id"]
                )

                request.session["usuario_email"] = (
                    usuario["email"]
                )

                return redirect("inicio")

            messages.error(
                request,
                "E-mail ou senha incorretos."
            )

    else:

        form = LoginForm()

    return render(
        request,
        "login/login.html",
        {
            "form": form
        }
    )


@require_POST
def logout_view(request):

    request.session.flush()

    return redirect("login")


def editLogin_view(request):
    if request.method == "POST":
        reset = PassEdit(request.POST)

        if reset.is_valid():
            email = reset.cleaned_data["emailrec"]

            if usuarios.find_one({"email": email}):
                codigo = str(random.randint(0, 9999)).zfill(4)
                request.session["codigo_recuperacao"] = codigo
                request.session["email"] = email
                send_mail(
                    "Código para mudar a senha",
                    f"Insira o código: {codigo}",
                    None,
                    [email],
                )
            else:
                messages.error(request, "E-mail não cadastrado.")
    else:
        reset = PassEdit()

    return render(
        request,
        "login/login.html",
        {"form": reset},
    )


def Check_view(request):
    if request.method == "POST":
        insert = CodeInput(request.POST)

        if insert.is_valid():
            codigo = request.session.get("codigo_recuperacao")
            try_code = insert.cleaned_data["code"]

            if codigo and codigo == try_code:
                return redirect("login/change.html",)

            messages.error(request, "Código inválido.")
    else:
        insert = CodeInput()

    return render(
        request,
        "login/check.html",
        {"form": insert},
    )

def Change_view(request):
    if request.method == "POST":
     var = ChangePass(request.POST)
    
     if var.is_valid():
        senha = var.cleaned_data["senha1"]
        confirmarSenha = var.cleaned_data["confirmarSenha"]
        email = request.session.get("email")
 
        if senha == confirmarSenha:
            usuarios.update_one(
             {"email": email},
                {
                  "$set": {
                      "senha": make_password(senha)
                           }
                      })

        else:
         messages.error(request, "senha inválida.")

        

     else:
            insert = CodeInput()
    
     return render(
            request,
            "login/change.html",
            {"form": insert},
        )
