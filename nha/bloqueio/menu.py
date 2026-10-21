import time
import psutil
from datetime import datetime
from cadastro.mongo import bloqueio_config


def bloquear():

    while True:

        regras = bloqueio_config.find({"ativo": True})

        for regra in regras:

            processo_alvo = regra["processo"]
            inicio = regra["hora_inicio"]
            fim = regra["hora_fim"]

            
            hAtual = datetime.now().strftime("%H:%M")

            
            if not inicio <= hAtual < fim:

                for processo in psutil.process_iter(["name"]):

                    try:
                        nome = processo.info["name"]

                        if nome and nome.lower() == processo_alvo.lower():
                            processo.terminate()

                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

        time.sleep(2)


bloquear()