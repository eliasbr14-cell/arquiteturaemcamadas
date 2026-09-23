"""
Camada de regras de negocio.

Aqui ficam as validacoes e os calculos do estacionamento. A interface grafica
chama estas funcoes, mas nao altera os dados diretamente.
"""

import math
import re
from datetime import datetime

import dados


VALOR_POR_HORA = 6.00

PADRAO_PLACA_ANTIGA = re.compile(r"^[A-Z]{3}[0-9]{4}$")
PADRAO_PLACA_MERCOSUL = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")


def normalizar_placa(placa):
    """Padroniza a placa para comparacao e armazenamento."""
    return placa.strip().upper().replace("-", "").replace(" ", "")


def validar_placa(placa):
    """Valida placas nos formatos AAA1234 e AAA1A23."""
    placa = normalizar_placa(placa)
    return bool(
        PADRAO_PLACA_ANTIGA.match(placa)
        or PADRAO_PLACA_MERCOSUL.match(placa)
    )


def ha_vaga_disponivel():
    """Verifica se o estacionamento ainda possui vagas livres."""
    return dados.total_estacionados() < dados.get_capacidade_total()


def vagas_disponiveis():
    """Calcula quantas vagas estao livres."""
    return dados.get_capacidade_total() - dados.total_estacionados()


def registrar_entrada(placa):
    """
    Registra a entrada de um veiculo, respeitando as regras do sistema.

    Retorna:
        tuple: (sucesso, mensagem)
    """
    placa = normalizar_placa(placa)

    if not validar_placa(placa):
        return False, "Placa invalida. Use o formato AAA1234 ou AAA1A23."

    if dados.buscar_veiculo(placa):
        return False, f"O veiculo {placa} ja esta estacionado."

    if not ha_vaga_disponivel():
        return False, "Estacionamento lotado. Nao ha vagas disponiveis."

    hora_entrada = datetime.now()
    dados.salvar_entrada(placa, hora_entrada)

    horario = hora_entrada.strftime("%H:%M:%S")
    return True, f"Entrada registrada para {placa} as {horario}."


def calcular_valor(hora_entrada, hora_saida):
    """Calcula as horas cobradas e o valor total a pagar."""
    tempo_total = hora_saida - hora_entrada
    horas = tempo_total.total_seconds() / 3600
    horas_cobradas = max(1, math.ceil(horas))
    valor = horas_cobradas * VALOR_POR_HORA

    return horas_cobradas, valor


def registrar_saida(placa):
    """
    Registra a saida de um veiculo e envia o movimento para o historico.

    Retorna:
        tuple: (sucesso, mensagem)
    """
    placa = normalizar_placa(placa)
    veiculo = dados.buscar_veiculo(placa)

    if not veiculo:
        return False, f"Veiculo {placa} nao encontrado no estacionamento."

    hora_entrada = veiculo["hora_entrada"]
    hora_saida = datetime.now()
    horas_cobradas, valor = calcular_valor(hora_entrada, hora_saida)

    registro = {
        "placa": placa,
        "hora_entrada": hora_entrada,
        "hora_saida": hora_saida,
        "horas_cobradas": horas_cobradas,
        "valor": valor,
    }

    dados.salvar_historico(registro)
    dados.remover_veiculo(placa)

    horario_saida = hora_saida.strftime("%H:%M:%S")
    mensagem = (
        f"Veiculo {placa} saiu as {horario_saida}.\n"
        f"Tempo cobrado: {horas_cobradas}h | Valor a pagar: R$ {valor:.2f}"
    )

    return True, mensagem
