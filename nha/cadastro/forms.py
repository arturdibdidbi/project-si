from django import forms
from django.core.validators import RegexValidator


class CadastroForm(forms.Form):

    nome = forms.CharField(
        max_length=50,
        label="nome"
    )

    email = forms.EmailField(
        label="email"
    )

    senha = forms.CharField(
        label="senha",
        min_length=8,
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).+$',
                message=(
                    'A senha deve conter no mínimo uma letra minúscula, '
                    'uma letra maiúscula, um número e um símbolo especial.'
                ),
            ),
        ],
    )

class ExcluirContaForm(forms.Form):

    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput
    )

