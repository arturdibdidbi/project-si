import psutil
from django import forms

from cadastro.mongo import bloqueio_config

PROCESSOS_PROTEGIDOS = {
    "system",
    "registry",
    "smss.exe",
    "csrss.exe",
    "wininit.exe",
    "services.exe",
    "lsass.exe",
    "winlogon.exe",
    "svchost.exe",
}


def listar_aplicativos():
    processos = set()

    for processo in psutil.process_iter(["name"]):
        try:
            nome = processo.info["name"]

            if not nome:
                continue

            nome = nome.strip()

            if not nome.lower().endswith(".exe"):
                continue

            if nome.lower() in PROCESSOS_PROTEGIDOS:
                continue

            processos.add(nome)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return sorted(processos, key=str.lower)


class BloqueioForm(forms.Form):

    aplicativo = forms.ChoiceField(
        choices=[],
        required=True,
        label="Aplicativo"
    )

    processo = forms.CharField(
        required=False,
        disabled=True,
        label="Processo selecionado"
    )

    tipo = forms.ChoiceField(
        choices=[
            ("padrao", "Padrão"),
            ("extremo", "Extremo"),
        ],
        required=True,
        label="Tipo de bloqueio"
    )

    hora_inicio = forms.TimeField(
        required=False,
        input_formats=["%H:%M"],
        widget=forms.TimeInput(
            format="%H:%M",
            attrs={"type": "time"}
        ),
        label="Horário inicial"
    )

    hora_fim = forms.TimeField(
        required=False,
        input_formats=["%H:%M"],
        widget=forms.TimeInput(
            format="%H:%M",
            attrs={"type": "time"}
        ),
        label="Horário final"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        processos = listar_aplicativos()

        self.fields["aplicativo"].choices = [
            (nome, nome) for nome in processos
        ]

        self.processos_disponiveis = set(processos)

    def clean(self):
        dados = super().clean()

        processo = dados.get("aplicativo")
        tipo = dados.get("tipo")
        inicio = dados.get("hora_inicio")
        fim = dados.get("hora_fim")

        if processo:
          
            processos_atuais = set(listar_aplicativos())

            if processo not in processos_atuais:
                self.add_error(
                    "aplicativo",
                    "Este processo não está mais em execução. "
                    "Atualize a página e selecione novamente."
                )
            else:
                existente = bloqueio_config.find_one({
                    "processo": processo
                })

                if existente:
                    self.add_error(
                        "aplicativo",
                        "Este processo já possui uma regra de bloqueio."
                    )

        if tipo == "extremo":
            if not inicio:
                self.add_error(
                    "hora_inicio",
                    "Informe o horário inicial."
                )

            if not fim:
                self.add_error(
                    "hora_fim",
                    "Informe o horário final."
                )

            if inicio and fim and inicio == fim:
                self.add_error(
                    "hora_fim",
                    "Os horários não podem ser iguais."
                )

        elif tipo == "padrao":
            if inicio or fim:
                self.add_error(
                    None,
                    "O modo Padrão não utiliza horários."
                )

        return dados