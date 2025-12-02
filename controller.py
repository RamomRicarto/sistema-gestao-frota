import os
import json

DATA_DIR = "data"
FILE_VEICULOS = os.path.join(DATA_DIR, "veiculos.json")
FILE_MOTORISTAS = os.path.join(DATA_DIR, "motoristas.json")
FILE_VIAGENS = os.path.join(DATA_DIR, "viagens.json")

def _criar_diretorio():
    """Cria a pasta 'data' se ela não existir (uso interno)."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def salvar_dados(dados: list, nome_arquivo: str):
    """
    Recebe uma lista de objetos, converte para dict e salva em JSON.
    """
    _criar_diretorio()

    lista_dicts = [item.to_dict() for item in dados]
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(lista_dicts, f, indent=4, ensure_ascii=False)

def carregar_dados_veiculos() -> list:
    """Lê o arquivo JSON de veículos e retorna a lista de dicionários."""
    if not os.path.exists(FILE_VEICULOS):
        return []
    try:
        with open(FILE_VEICULOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
