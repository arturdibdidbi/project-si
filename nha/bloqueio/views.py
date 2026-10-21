from django.shortcuts import render, redirect
from bson import ObjectId
from datetime import datetime
from cadastro.mongo import bloqueio_config


from .forms import BloqueioForm
from cadastro.mongo import bloqueio_config


def bloqueio(request):
    regras = list(bloqueio_config.find())

    return render(
        request,
        "bloqueio/bloqueio.html",
        {"regras": regras}
    )


def criar_bloqueio(request):
    if request.method == "POST":
        form = BloqueioForm(request.POST)

        if form.is_valid():
            processo = form.cleaned_data["aplicativo"]
            tipo = form.cleaned_data["tipo"]

            regra = {
                "aplicativo": processo,
                "processo": processo,
                "tipo": tipo,
                "ativo": False,
                "bloqueado": False,
            }

            if tipo == "extremo":
                regra["hora_inicio"] = (
                    form.cleaned_data["hora_inicio"].strftime("%H:%M")
                )
                regra["hora_fim"] = (
                    form.cleaned_data["hora_fim"].strftime("%H:%M")
                )

            bloqueio_config.insert_one(regra)

            return redirect("bloqueio")

    else:
        form = BloqueioForm()

    return render(
        request,
        "bloqueio/criar_regra.html",
        {"form": form}
    )


def bloquear(request, id):
    bloqueio_config.update_one(
        {"_id": ObjectId(id), "tipo": "padrao"},
        {"$set": {"bloqueado": True, "ativo": True}}
    )

    return redirect("bloqueio")


def desbloquear(request, id):
    bloqueio_config.update_one(
        {"_id": ObjectId(id), "tipo": "padrao"},
        {"$set": {"bloqueado": False, "ativo": False}}
    )

    return redirect("bloqueio")

historico = bloqueio_config.database["bloqueio_historico"]

def ver_historico(request):
    eventos = list(
        historico.find().sort("data_hora", -1)
    )

    return render(
        request,
        "bloqueio/historico.html",
        {"eventos": eventos}
    )