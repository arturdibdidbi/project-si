from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from .forms import CadastroForm, ExcluirContaForm
from .mongo import usuarios

from pymongo.errors import DuplicateKeyError

from bson import ObjectId
from bson.errors import InvalidId

from objetivos.mongo import objetivos, marcos, tarefas


def cadastro(request):

    if request.method == "POST":

        form = CadastroForm(request.POST)

        if form.is_valid():

            nome = form.cleaned_data["nome"]
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]

            hashed_senha = make_password(senha)

            usuario = {
                "nome": nome,
                "email": email,
                "senha": hashed_senha
            }

            try:

                usuarios.insert_one(usuario)

                return redirect("login")

            except DuplicateKeyError:

                form.add_error(
                    "email",
                    "Este e-mail já está cadastrado."
                )

    else:

        form = CadastroForm()

    return render(
        request,
        "cadastro/cadastro.html",
        {
            "form": form
        }
    )


def excluir_conta(request):

    usuario_id = request.session.get(
        "usuario_id"
    )

    if not usuario_id:
        return redirect("login")

    try:

        usuario_id_obj = ObjectId(
            usuario_id
        )

    except (InvalidId, TypeError):

        request.session.flush()

        return redirect("login")

    usuario = usuarios.find_one({
        "_id": usuario_id_obj
    })

    if not usuario:

        request.session.flush()

        return redirect("login")

    if request.method == "POST":

        form = ExcluirContaForm(
            request.POST
        )

        if form.is_valid():

            senha = form.cleaned_data[
                "senha"
            ]

            senha_correta = check_password(
                senha,
                usuario["senha"]
            )

            if senha_correta:

                # Exclui os objetivos
                objetivos.delete_many({
                    "usuario_id": usuario_id
                })

                # Exclui os marcos
                marcos.delete_many({
                    "usuario_id": usuario_id
                })

                # Exclui as tarefas
                tarefas.delete_many({
                    "usuario_id": usuario_id
                })

                # Exclui o usuário
                usuarios.delete_one({
                    "_id": usuario_id_obj
                })

                # Encerra a sessão
                request.session.flush()

                return redirect("login")

            form.add_error(
                "senha",
                "Senha incorreta."
            )

    else:

        form = ExcluirContaForm()

    return render(
        request,
        "cadastro/excluir_conta.html",
        {
            "form": form
        }
    )