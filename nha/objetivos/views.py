from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST

from bson import ObjectId
from bson.errors import InvalidId

from .forms import (
    ObjetivoForm,
    MarcoForm,
    TarefaForm
)

from .mongo import (
    objetivos,
    marcos,
    tarefas
)


def usuario_logado(request):

    return request.session.get("usuario_id")


def converter_id(valor):

    try:
        return ObjectId(valor)

    except (InvalidId, TypeError):

        return None



def inicio(request):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    lista_objetivos = list(
        objetivos.find({
            "usuario_id": usuario_id
        })
    )

    for objetivo in lista_objetivos:

        objetivo["id"] = str(
            objetivo["_id"]
        )

    return render(
        request,
        "objetivos/inicio.html",
        {
            "objetivos": lista_objetivos
        }
    )




def criar_objetivo(request):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    if request.method == "POST":

        form = ObjetivoForm(request.POST)

        if form.is_valid():

            resultado = objetivos.insert_one({

                "usuario_id": usuario_id,

                "area": form.cleaned_data["area"],

                "titulo": form.cleaned_data["titulo"],

                "descricao": form.cleaned_data["descricao"],

                "criado_em": timezone.now()

            })

            messages.success(
                request,
                "Objetivo criado com sucesso!"
            )

            return redirect(
                "objetivo",
                objetivo_id=str(
                    resultado.inserted_id
                )
            )

    else:

        form = ObjetivoForm()

    return render(
        request,
        "objetivos/criar_objetivo.html",
        {
            "form": form
        }
    )




def objetivo(request, objetivo_id):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    objetivo_id_obj = converter_id(
        objetivo_id
    )

    if not objetivo_id_obj:
        return redirect("inicio")

    objetivo_data = objetivos.find_one({
        "_id": objetivo_id_obj,
        "usuario_id": usuario_id
    })

    if not objetivo_data:
        return redirect("inicio")

    objetivo_data["id"] = str(
        objetivo_data["_id"]
    )

    lista_marcos = list(
        marcos.find({
            "objetivo_id": str(
                objetivo_id_obj
            ),
            "usuario_id": usuario_id
        })
    )

    lista_tarefas = list(
        tarefas.find({
            "objetivo_id": str(
                objetivo_id_obj
            ),
            "usuario_id": usuario_id
        })
    )

    for marco in lista_marcos:

        marco["id"] = str(
            marco["_id"]
        )

    for tarefa in lista_tarefas:

        tarefa["id"] = str(
            tarefa["_id"]
        )

    return render(
        request,
        "objetivos/objetivo.html",
        {
            "objetivo": objetivo_data,
            "marcos": lista_marcos,
            "tarefas": lista_tarefas
        }
    )




def editar_objetivo(request, objetivo_id):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    objetivo_id_obj = converter_id(
        objetivo_id
    )

    if not objetivo_id_obj:
        return redirect("inicio")

    objetivo_data = objetivos.find_one({
        "_id": objetivo_id_obj,
        "usuario_id": usuario_id
    })

    if not objetivo_data:
        return redirect("inicio")

    if request.method == "POST":

        form = ObjetivoForm(
            request.POST
        )

        if form.is_valid():

            objetivos.update_one(

                {
                    "_id": objetivo_id_obj,
                    "usuario_id": usuario_id
                },

                {
                    "$set": {

                        "area": form.cleaned_data["area"],

                        "titulo": form.cleaned_data["titulo"],

                        "descricao": form.cleaned_data["descricao"]

                    }
                }
            )

            messages.success(
                request,
                "Objetivo atualizado com sucesso!"
            )

            return redirect(
                "objetivo",
                objetivo_id=objetivo_id
            )

    else:

        form = ObjetivoForm(
            initial={
                "area": objetivo_data["area"],
                "titulo": objetivo_data["titulo"],
                "descricao": objetivo_data.get(
                    "descricao",
                    ""
                )
            }
        )

    objetivo_data["id"] = str(
        objetivo_data["_id"]
    )

    return render(
        request,
        "objetivos/editar_objetivo.html",
        {
            "form": form,
            "objetivo": objetivo_data
        }
    )




@require_POST
def excluir_objetivo(request, objetivo_id):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    objetivo_id_obj = converter_id(
        objetivo_id
    )

    if not objetivo_id_obj:
        return redirect("inicio")

    objetivo_data = objetivos.find_one({
        "_id": objetivo_id_obj,
        "usuario_id": usuario_id
    })

    if not objetivo_data:
        return redirect("inicio")

    tarefas.delete_many({
        "objetivo_id": str(
            objetivo_id_obj
        ),
        "usuario_id": usuario_id
    })

    marcos.delete_many({
        "objetivo_id": str(
            objetivo_id_obj
        ),
        "usuario_id": usuario_id
    })

    objetivos.delete_one({
        "_id": objetivo_id_obj,
        "usuario_id": usuario_id
    })

    messages.success(
        request,
        "Objetivo excluído com sucesso."
    )

    return redirect("inicio")



def criar_marco(request, objetivo_id):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    objetivo_id_obj = converter_id(
        objetivo_id
    )

    if not objetivo_id_obj:
        return redirect("inicio")

    objetivo_data = objetivos.find_one({
        "_id": objetivo_id_obj,
        "usuario_id": usuario_id
    })

    if not objetivo_data:
        return redirect("inicio")

    if request.method == "POST":

        form = MarcoForm(
            request.POST
        )

        if form.is_valid():

            marcos.insert_one({

                "usuario_id": usuario_id,

                "objetivo_id": str(
                    objetivo_id_obj
                ),

                "titulo": form.cleaned_data["titulo"],

                "descricao": form.cleaned_data["descricao"],

                "criado_em": timezone.now()

            })

            messages.success(
                request,
                "Marco criado com sucesso!"
            )

            return redirect(
                "objetivo",
                objetivo_id=objetivo_id
            )

    else:

        form = MarcoForm()

    objetivo_data["id"] = str(
        objetivo_data["_id"]
    )

    return render(
        request,
        "objetivos/criar_marco.html",
        {
            "form": form,
            "objetivo": objetivo_data
        }
    )



def criar_tarefa(request, objetivo_id):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    objetivo_id_obj = converter_id(
        objetivo_id
    )

    if not objetivo_id_obj:
        return redirect("inicio")

    objetivo_data = objetivos.find_one({
        "_id": objetivo_id_obj,
        "usuario_id": usuario_id
    })

    if not objetivo_data:
        return redirect("inicio")

    lista_marcos = list(
        marcos.find({
            "objetivo_id": str(
                objetivo_id_obj
            ),
            "usuario_id": usuario_id
        })
    )

    for marco in lista_marcos:

        marco["id"] = str(
            marco["_id"]
        )

    if request.method == "POST":

        form = TarefaForm(
            request.POST
        )

        if form.is_valid():

            marco_id = request.POST.get(
                "marco_id"
            )

            if marco_id:

                marco_id_obj = converter_id(
                    marco_id
                )

                marco_existe = marcos.find_one({
                    "_id": marco_id_obj,
                    "objetivo_id": str(
                        objetivo_id_obj
                    ),
                    "usuario_id": usuario_id
                })

                if not marco_existe:

                    form.add_error(
                        None,
                        "Marco inválido."
                    )

                else:

                    tarefas.insert_one({

                        "usuario_id": usuario_id,

                        "objetivo_id": str(
                            objetivo_id_obj
                        ),

                        "marco_id": marco_id,

                        "area": objetivo_data["area"],

                        "titulo": form.cleaned_data["titulo"],

                        "descricao": form.cleaned_data["descricao"],

                        "concluida": False,

                        "criado_em": timezone.now()

                    })

                    messages.success(
                        request,
                        "Tarefa criada com sucesso!"
                    )

                    return redirect(
                        "objetivo",
                        objetivo_id=objetivo_id
                    )

            else:

                tarefas.insert_one({

                    "usuario_id": usuario_id,

                    "objetivo_id": str(
                        objetivo_id_obj
                    ),

                    "marco_id": None,

                    "area": objetivo_data["area"],

                    "titulo": form.cleaned_data["titulo"],

                    "descricao": form.cleaned_data["descricao"],

                    "concluida": False,

                    "criado_em": timezone.now()

                })

                messages.success(
                    request,
                    "Tarefa criada com sucesso!"
                )

                return redirect(
                    "objetivo",
                    objetivo_id=objetivo_id
                )

    else:

        form = TarefaForm()

    objetivo_data["id"] = str(
        objetivo_data["_id"]
    )

    return render(
        request,
        "objetivos/criar_tarefa.html",
        {
            "form": form,
            "objetivo": objetivo_data,
            "marcos": lista_marcos
        }
    )



@require_POST
def concluir_tarefa(request, tarefa_id):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    tarefa_id_obj = converter_id(
        tarefa_id
    )

    if not tarefa_id_obj:
        return redirect("inicio")

    tarefa = tarefas.find_one({
        "_id": tarefa_id_obj,
        "usuario_id": usuario_id
    })

    if not tarefa:
        return redirect("inicio")

    novo_estado = not tarefa.get(
        "concluida",
        False
    )

    tarefas.update_one(

        {
            "_id": tarefa_id_obj,
            "usuario_id": usuario_id
        },

        {
            "$set": {
                "concluida": novo_estado
            }
        }
    )

    return redirect(
        "objetivo",
        objetivo_id=tarefa["objetivo_id"]
    )




@require_POST
def excluir_tarefa(request, tarefa_id):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    tarefa_id_obj = converter_id(
        tarefa_id
    )

    if not tarefa_id_obj:
        return redirect("inicio")

    tarefa = tarefas.find_one({
        "_id": tarefa_id_obj,
        "usuario_id": usuario_id
    })

    if not tarefa:
        return redirect("inicio")

    tarefas.delete_one({
        "_id": tarefa_id_obj,
        "usuario_id": usuario_id
    })

    return redirect(
        "objetivo",
        objetivo_id=tarefa["objetivo_id"]
    )



def graficos(request):

    usuario_id = usuario_logado(request)

    if not usuario_id:
        return redirect("login")

    areas = [
        "Finanças",
        "Trabalho",
        "Estudo",
        "Saúde",
        "Lazer"
    ]

    pontuacao = {}

    for area in areas:

        pontuacao[area] = tarefas.count_documents({

            "usuario_id": usuario_id,

            "area": area,

            "concluida": True

        })

    return render(
        request,
        "objetivos/graficos.html",
        {
            "pontuacao": pontuacao
        }
    )