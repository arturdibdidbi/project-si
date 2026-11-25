from django.shortcuts import render, redirect
from bson import ObjectId
from datetime import datetime
from cadastro.mongo import bloqueio_config


from .forms import BloqueioForm
from cadastro.mongo import bloqueio_config







def bloqueio(request):
    regras = list(bloqueio_config.find())

    for regra in regras:
        regra["id"] = str(regra["_id"])

    return render(request, "bloqueio.html", {"regras": regras})


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
                "ativo": tipo == "extremo",
                "bloqueado": False,
            }

            if tipo == "extremo":
                regra["hora_inicio"] = form.cleaned_data["hora_inicio"].strftime("%H:%M")
                regra["hora_fim"] = form.cleaned_data["hora_fim"].strftime("%H:%M")

            bloqueio_config.insert_one(regra)
            return redirect("bloqueio")

    else:
        tipo = request.GET.get("tipo", "padrao")
        form = BloqueioForm(initial={"tipo": tipo})

    tipo_selecionado = (
        form.data.get("tipo") if form.is_bound
        else form.initial.get("tipo", "padrao")
    )

    return render(request, "criar.html", {
        "form": form,
        "tipo_selecionado": tipo_selecionado,
    })

def bloquear(request, id):

    regra = bloqueio_config.find_one({
        "_id": ObjectId(id),
        "tipo": "padrao"
    })

    if regra:
        bloqueio_config.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "bloqueado": True,
                "ativo": True
            }}
        )
        

        registrar_evento(
            regra["aplicativo"],
            "Bloqueio ativado"
        )

    return redirect("bloqueio")


def desbloquear(request, id):

    regra = bloqueio_config.find_one({
        "_id": ObjectId(id),
        "tipo": "padrao"
    })

    if regra:
        bloqueio_config.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "bloqueado": False,
                "ativo": False
            }}
        )

        registrar_evento(
            regra["aplicativo"],
            "Bloqueio desativado"
        )

    return redirect("bloqueio")

historico = bloqueio_config.database["bloqueio_historico"]


def registrar_evento(aplicativo, acao):
    historico.insert_one({
        "aplicativo": aplicativo,
        "acao": acao,
        "data_hora": datetime.now()

    })

def registrar_evento(aplicativo, acao):
    historico.insert_one({
        "aplicativo": aplicativo,
        "acao": acao,
        "data_hora": datetime.now()
    })

def ver_historico(request):
    eventos = list(
        historico.find().sort("data_hora", -1)
    )

    return render(
        request,
        "historico.html",
        {"eventos": eventos}
    )