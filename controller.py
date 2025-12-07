import os
import json
from models import Veiculo, Motorista, Viagem, AlocacaoInvalidaError, ManutencaoInvalidaError, Carro, Moto, Caminhao

DATA_DIR = "data"
FILE_VEICULOS = os.path.join(DATA_DIR, "veiculos.json")
FILE_MOTORISTAS = os.path.join(DATA_DIR, "motoristas.json")
FILE_VIAGENS = os.path.join(DATA_DIR, "viagens.json")
FILE_SETTINGS = "settings.json"

def _criar_diretorio():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def salvar_objetos(lista_objetos, arquivo):
    """Salva lista de objetos no JSON."""
    _criar_diretorio()
    lista_dicts = [item.to_dict() for item in lista_objetos]
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(lista_dicts, f, indent=4, ensure_ascii=False)

def carregar_veiculos() -> list:
    """Retorna lista de OBJETOS Veiculo."""
    if not os.path.exists(FILE_VEICULOS): return []
    try:
        with open(FILE_VEICULOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return [Veiculo.from_dict(d) for d in dados]
    except Exception as e:
        print(f"Erro ao carregar veículos: {e}")
        return []

def carregar_motoristas() -> list:
    """Retorna lista de OBJETOS Motorista."""
    if not os.path.exists(FILE_MOTORISTAS): return []
    try:
        with open(FILE_MOTORISTAS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return [Motorista.from_dict(d) for d in dados]
    except Exception:
        return []

def buscar_veiculo(placa, lista_veiculos):
    for v in lista_veiculos:
        if v.placa == placa:
            return v
    return None

def buscar_motorista(cpf, lista_motoristas):
    for m in lista_motoristas:
        if m.cpf == cpf:
            return m
    return None

def carregar_viagens_dicts():
    if not os.path.exists(FILE_VIAGENS):
        return []
    try:
        with open(FILE_VIAGENS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_viagens_dicts(lista_dicts):
    _criar_diretorio()
    with open(FILE_VIAGENS, "w", encoding="utf-8") as f:
        json.dump(lista_dicts, f, indent=4, ensure_ascii=False)

def realizar_viagem_controller(cpf, placa, destino, distancia):
    motoristas = carregar_motoristas()
    veiculos = carregar_veiculos()
    
    mot = buscar_motorista(cpf, motoristas)
    veic = buscar_veiculo(placa, veiculos)
    
    if not mot:
        raise Exception(f"Motorista com CPF {cpf} não encontrado.")
    if not veic:
        raise Exception(f"Veículo com placa {placa} não encontrado.")

    viagem = Viagem(mot, veic, destino, float(distancia))
    viagem.realizar_viagem()
    
    salvar_objetos(veiculos, FILE_VEICULOS)
    
    historico = carregar_viagens_dicts()
    historico.append(viagem.to_dict())
    salvar_viagens_dicts(historico)
    
    return f"Viagem registrada para {destino}! Nova KM: {veic.quilometragem}"

def realizar_manutencao_controller(placa):
    veiculos = carregar_veiculos()
    veic = buscar_veiculo(placa, veiculos)
    
    if not veic:
        raise Exception("Veículo não encontrado.")
    
    veic.registrar_manutencao()
    
    salvar_objetos(veiculos, FILE_VEICULOS)
    return f"Veículo {placa} enviado para manutenção."

def finalizar_manutencao_controller(placa):
    veiculos = carregar_veiculos()
    veic = buscar_veiculo(placa, veiculos)
    
    if not veic: raise Exception("Veículo não encontrado.")
    
    veic.finalizar_manutencao()
    salvar_objetos(veiculos, FILE_VEICULOS)
    return f"Veículo {placa} liberado da manutenção."

def cadastrar_veiculo_controller(tipo, placa, marca, modelo, ano, km_inicial):
    veiculos = carregar_veiculos()
    
    if buscar_veiculo(placa, veiculos):
        raise Exception(f"Veículo com placa {placa} já existe!")

    if tipo.lower() == "carro":
        novo_veiculo = Carro(placa, marca, modelo, int(ano), float(km_inicial))
    elif tipo.lower() == "moto":
        novo_veiculo = Moto(placa, marca, modelo, int(ano), float(km_inicial))
    elif tipo.lower() in ["caminhão", "caminhao"]:
        novo_veiculo = Caminhao(placa, marca, modelo, int(ano), float(km_inicial))
    else:
        raise Exception("Tipo de veículo inválido. Use: Carro, Moto ou Caminhão")

    veiculos.append(novo_veiculo)
    salvar_objetos(veiculos, FILE_VEICULOS)
    return f"{tipo} {modelo} cadastrado com sucesso!"

def cadastrar_motorista_controller(nome, cpf, cnh, categoria):
    motoristas = carregar_motoristas()
    
    if buscar_motorista(cpf, motoristas):
        raise Exception(f"Motorista com CPF {cpf} já existe!")

    novo_motorista = Motorista(nome, cpf, cnh, categoria)
    motoristas.append(novo_motorista)
    
    salvar_objetos(motoristas, FILE_MOTORISTAS)
    return f"Motorista {nome} cadastrado com sucesso!"