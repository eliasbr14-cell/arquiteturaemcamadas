"""
Camada de dados do sistema.

Neste projeto, os dados ficam guardados em memoria enquanto o programa esta
aberto. Esta camada nao faz validacoes e nao conversa com o usuario.
"""

CAPACIDADE_TOTAL = 20

veiculos_estacionados = {}
historico_saidas = []


def salvar_entrada(placa, hora_entrada):
    """Guarda um veiculo na lista de estacionados."""
    veiculos_estacionados[placa] = {"hora_entrada": hora_entrada}


def buscar_veiculo(placa):
    """Busca um veiculo pela placa."""
    return veiculos_estacionados.get(placa)


def remover_veiculo(placa):
    """Remove um veiculo estacionado."""
    veiculos_estacionados.pop(placa, None)


def salvar_historico(registro):
    """Guarda o registro de saida de um veiculo."""
    historico_saidas.append(registro)


def listar_veiculos_estacionados():
    """Retorna os veiculos que ainda estao no estacionamento."""
    return veiculos_estacionados


def listar_historico():
    """Retorna os registros de saida."""
    return historico_saidas


def total_estacionados():
    """Retorna a quantidade de veiculos estacionados."""
    return len(veiculos_estacionados)


def get_capacidade_total():
    """Retorna a capacidade maxima do estacionamento."""
    return CAPACIDADE_TOTAL
