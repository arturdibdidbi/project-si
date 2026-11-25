from django import forms


AREAS = [
    ("Finanças", "Finanças"),
    ("Trabalho", "Trabalho"),
    ("Estudo", "Estudo"),
    ("Saúde", "Saúde"),
    ("Lazer", "Lazer"),
]


class ObjetivoForm(forms.Form):

    area = forms.ChoiceField(
        choices=AREAS,
        label="Área"
    )

    titulo = forms.CharField(
        max_length=150,
        label="Objetivo"
    )

    descricao = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Descrição"
    )


class MarcoForm(forms.Form):

    titulo = forms.CharField(
        max_length=150,
        label="Marco"
    )

    descricao = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Descrição"
    )


class TarefaForm(forms.Form):

    titulo = forms.CharField(
        max_length=150,
        label="Tarefa"
    )

    descricao = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Descrição"
    )

    prazo = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"}
        ),
        label="Prazo"
    )

class ExcluirContaForm(forms.Form):

    senha = forms.CharField(
        label="Senha atual",
        widget=forms.PasswordInput
    )

class EditarPerfilForm(forms.Form):
    nome = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField(label="E-mail")
