from typing import List, Dict, Any

def exibir_cabecalho():
    print("=== SISTEMA DE GESTÃO DE FROTA ===\n")

def exibir_mensagem_salvamento(nome_arquivo: str):
    print(f"Dados salvos com sucesso em: {nome_arquivo}")

def exibir_inicio_salvamento():
    print("--- Salvando Dados ---")

def exibir_relatorio_frota(dados_veiculos: List[Dict[str, Any]]):
    """
    Exibe o relatório formatado a partir de uma lista de dicionários 
    (formato vindo do JSON).
    """
    print("\n--- Relatório da Frota (Dados em Disco) ---")
    if not dados_veiculos:
        print("Nenhum veículo encontrado no registro.")
        return

    for item in dados_veiculos:
        modelo = item.get('modelo', 'Desconhecido')
        marca = item.get('marca', '')
        placa = item.get('placa', '---')
        km = item.get('quilometragem', 0)
        
        print(f"Veículo: {modelo} ({marca}) | Placa: {placa} | KM: {km}")

def exibir_relatorio_viagens(viagens: List[Any]):
    """
    Exibe o relatório a partir de uma lista de objetos Viagem.
    """
    print("\n--- Relatório de Viagens Recentes ---")
    if not viagens:
        print("Nenhuma viagem recente registrada.")
        return

    for v in viagens:
        print(v)