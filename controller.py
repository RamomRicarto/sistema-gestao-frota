import os
import json
from models import (
    Veiculo, Motorista, Viagem, Carro, Moto, Caminhao, 
    Manutencao, Abastecimento, AlocacaoInvalidaError, ManutencaoInvalidaError
)

DATA_DIR = "data"
FILE_VEICULOS = os.path.join(DATA_DIR, "veiculos.json")
FILE_MOTORISTAS = os.path.join(DATA_DIR, "motoristas.json")
FILE_VIAGENS = os.path.join(DATA_DIR, "viagens.json")

def _criar_diretorio():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def salvar_objetos(lista_objetos, arquivo):
    _criar_diretorio()
    lista_dicts = [item.to_dict() for item in lista_objetos]
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(lista_dicts, f, indent=4, ensure_ascii=False)

def carregar_veiculos() -> list:
    if not os.path.exists(FILE_VEICULOS): return []
    try:
        with open(FILE_VEICULOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return [Veiculo.from_dict(d) for d in dados]
    except Exception as e:
        print(f"Erro ao carregar veículos: {e}")
        return []

def carregar_motoristas() -> list:
    if not os.path.exists(FILE_MOTORISTAS): return []
    try:
        with open(FILE_MOTORISTAS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return [Motorista.from_dict(d) for d in dados]
    except Exception:
        return []

def carregar_viagens_dicts():
    if not os.path.exists(FILE_VIAGENS): return []
    try:
        with open(FILE_VIAGENS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_viagens_dicts(lista_dicts):
    _criar_diretorio()
    with open(FILE_VIAGENS, "w", encoding="utf-8") as f:
        json.dump(lista_dicts, f, indent=4, ensure_ascii=False)

def buscar_veiculo(placa, lista_veiculos=None):
    if lista_veiculos is None: lista_veiculos = carregar_veiculos()
    for v in lista_veiculos:
        if v.placa.upper() == placa.upper(): return v
    return None

def buscar_motorista(cpf, lista_motoristas=None):
    if lista_motoristas is None: lista_motoristas = carregar_motoristas()
    for m in lista_motoristas:
        if m.cpf == cpf: return m
    return None

def cadastrar_veiculo_controller(tipo, placa, marca, modelo, ano, km_inicial):
    veiculos = carregar_veiculos()
    if buscar_veiculo(placa, veiculos):
        raise Exception(f"Veículo com placa {placa} já existe!")

    tipo = tipo.capitalize()
    if tipo == "Carro": cls = Carro
    elif tipo == "Moto": cls = Moto
    elif tipo in ["Caminhão", "Caminhao"]: cls = Caminhao
    else: raise Exception("Tipo inválido. Use Carro, Moto ou Caminhão.")

    try:
        novo = cls(placa, marca, modelo, int(ano), float(km_inicial))
        veiculos.append(novo)
        salvar_objetos(veiculos, FILE_VEICULOS)
        return "Veículo cadastrado com sucesso!"
    except ValueError:
        raise Exception("Ano ou KM devem ser números válidos.")

def cadastrar_motorista_controller(nome, cpf, cnh, categoria):
    motoristas = carregar_motoristas()
    if buscar_motorista(cpf, motoristas):
        raise Exception(f"Motorista CPF {cpf} já existe!")
    
    novo = Motorista(nome, cpf, cnh, categoria)
    motoristas.append(novo)
    salvar_objetos(motoristas, FILE_MOTORISTAS)
    return "Motorista cadastrado com sucesso!"

def atualizar_veiculo_controller(placa, nova_marca, novo_modelo, novo_ano):
    veiculos = carregar_veiculos()
    veic = buscar_veiculo(placa, veiculos)
    if not veic: raise Exception("Veículo não encontrado.")

    alterado = False
    if nova_marca: 
        veic.marca = nova_marca
        alterado = True
    if novo_modelo: 
        veic.modelo = novo_modelo
        alterado = True
    if novo_ano: 
        veic.ano = int(novo_ano)
        alterado = True
    
    if alterado:
        salvar_objetos(veiculos, FILE_VEICULOS)
        return f"Veículo {placa} atualizado."
    return "Nenhuma alteração realizada."

def atualizar_motorista_controller(cpf, novo_nome, nova_cnh, nova_cat):
    motoristas = carregar_motoristas()
    mot = buscar_motorista(cpf, motoristas)
    if not mot: raise Exception("Motorista não encontrado.")

    alterado = False
    if novo_nome: 
        mot.nome = novo_nome
        alterado = True
    if nova_cnh: 
        mot.cnh = nova_cnh
        alterado = True
    if nova_cat: 
        mot.categoria_cnh = nova_cat.upper()
        alterado = True

    if alterado:
        salvar_objetos(motoristas, FILE_MOTORISTAS)
        return f"Motorista {cpf} atualizado."
    return "Nenhuma alteração realizada."

def realizar_viagem_controller(cpf, placa, destino, distancia):
    motoristas = carregar_motoristas()
    veiculos = carregar_veiculos()
    
    mot = buscar_motorista(cpf, motoristas)
    veic = buscar_veiculo(placa, veiculos)
    
    if not mot: raise Exception(f"Motorista CPF {cpf} não encontrado.")
    if not veic: raise Exception(f"Veículo Placa {placa} não encontrado.")

    viagem = Viagem(mot, veic, destino, float(distancia))
    viagem.realizar_viagem()
    
    salvar_objetos(veiculos, FILE_VEICULOS)
    
    historico = carregar_viagens_dicts()
    historico.append(viagem.to_dict())
    salvar_viagens_dicts(historico)
    
    return f"Viagem registrada! Nova KM do veículo: {veic.quilometragem}"

def registrar_manutencao_controller(placa, data, tipo, custo, descricao):
    veiculos = carregar_veiculos()
    veic = buscar_veiculo(placa, veiculos)
    if not veic: raise Exception("Veículo não encontrado.")

    manutencao = Manutencao(data, tipo, float(custo), descricao)
    veic.adicionar_manutencao(manutencao)
    
    salvar_objetos(veiculos, FILE_VEICULOS)
    return f"Manutenção ({tipo}) registrada. Custo final calculado: R$ {manutencao.custo_final:.2f}"

def finalizar_manutencao_controller(placa):
    veiculos = carregar_veiculos()
    veic = buscar_veiculo(placa, veiculos)
    if not veic: raise Exception("Veículo não encontrado.")
    
    veic.finalizar_manutencao_status()
    salvar_objetos(veiculos, FILE_VEICULOS)
    return f"Veículo {placa} liberado da manutenção com sucesso."

def registrar_abastecimento_controller(placa, data, combustivel, litros, valor):
    veiculos = carregar_veiculos()
    veic = buscar_veiculo(placa, veiculos)
    if not veic: raise Exception("Veículo não encontrado.")

    abast = Abastecimento(data, combustivel, float(litros), float(valor))
    veic.abastecer(abast)
    
    salvar_objetos(veiculos, FILE_VEICULOS)
    return f"Abastecimento registrado para o veículo {placa}."

def gerar_relatorio_custos():
    """Retorna lista com custo total de manutenção por veículo."""
    veiculos = carregar_veiculos()
    relatorio = []
    
    for v in veiculos:
        total = sum(m.custo_final for m in v) 
        relatorio.append({
            "placa": v.placa,
            "modelo": v.modelo,
            "total_manutencao": total,
            "qtd_manutencoes": len(v.historico_manutencoes)
        })
    return relatorio

def gerar_relatorio_eficiencia():
    """
    Retorna eficiência (km/l) estimada e ordena (Ranking).
    CORREÇÃO IMPORTANTE: Usa (KM Atual - KM Entrada) / Litros Totais.
    """
    veiculos = carregar_veiculos()
    relatorio = []
    
    for v in veiculos:
        total_litros = sum(a.litros for a in v.historico_abastecimentos)
        
        km_inicial_real = getattr(v, 'km_entrada', 0)
        distancia_percorrida = v.quilometragem - km_inicial_real
        
        if total_litros > 0 and distancia_percorrida > 0:
            km_l = distancia_percorrida / total_litros
        else:
            km_l = 0.0
            
        relatorio.append({
            "placa": v.placa,
            "modelo": v.modelo,
            "litros": total_litros,
            "km_l": km_l
        })
    
    relatorio.sort(key=lambda x: x['km_l'], reverse=True)
    return relatorio