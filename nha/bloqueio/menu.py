import time
import psutil

from datetime import datetime
from cadastro.mongo import bloqueio_config


historico = bloqueio_config.database["bloqueio_historico"]


def registrar_evento(aplicativo, acao):

    historico.insert_one({
        "aplicativo": aplicativo,
        "acao": acao,
        "data_hora": datetime.now()
    })


def dentro_do_horario(inicio, fim):

    atual = datetime.now().strftime("%H:%M")

    if inicio < fim:
        return inicio <= atual < fim

    return atual >= inicio or atual < fim


def bloquear():

    eventos_registrados = set()

    print("Monitor de bloqueios iniciado.")

    while True:

        regras = list(
            bloqueio_config.find({
                "ativo": True
            })
        )

        processos_encontrados = set()

        for regra in regras:

            processo_alvo = regra.get("processo")

            if not processo_alvo:
                continue

            tipo = regra.get("tipo")

            if tipo == "padrao":

                deve_bloquear = regra.get(
                    "bloqueado",
                    True
                )

            elif tipo == "extremo":

                inicio = regra.get("hora_inicio")
                fim = regra.get("hora_fim")

                if not inicio or not fim:
                    continue

                deve_bloquear = dentro_do_horario(
                    inicio,
                    fim
                )

            else:
                continue

            if not deve_bloquear:
                continue

            for processo in psutil.process_iter(["pid", "name"]):

                try:

                    nome = processo.info["name"]

                    if not nome:
                        continue

                    if nome.lower() != processo_alvo.lower():
                        continue

                    chave = (
                        str(regra["_id"]),
                        processo.pid
                    )

                    processos_encontrados.add(chave)

                    processo.terminate()

                    try:
                        processo.wait(timeout=3)

                    except psutil.TimeoutExpired:
                        processo.kill()
                        processo.wait(timeout=3)

                    if chave not in eventos_registrados:

                        registrar_evento(
                            processo_alvo,
                            f"Processo encerrado automaticamente ({tipo})"
                        )

                        eventos_registrados.add(chave)

                        print(
                            f"Bloqueado: {processo_alvo}"
                        )

                except psutil.NoSuchProcess:
                    continue

                except psutil.AccessDenied:
                    print(
                        f"Permissão negada: {processo_alvo}"
                    )

                except psutil.Error:
                    continue

        eventos_registrados.intersection_update(
            processos_encontrados
        )

        time.sleep(2)


if __name__ == "__main__":
    bloquear()