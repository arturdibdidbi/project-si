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