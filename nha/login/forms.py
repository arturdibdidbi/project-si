from django import forms
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)



class PassEdit(forms.Form):
    emailrec = forms.EmailField()

class CodeInput(forms.Form):
    code = forms.CharField(max_length=4,
                           validators=[
                                       RegexValidator(
                                           regex=r'^\d{4}$')])

class ChangePass(forms.Form):
    senha1 = forms.CharField(label="senha",
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
    confirmarSenha = forms.CharField(widget=forms.PasswordInput)