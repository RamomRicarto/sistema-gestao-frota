from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AlocacaoInvalidaError(Exception):
    pass

class ManutencaoInvalidaError(Exception):
    pass

class OperacaoInvalidaError(Exception):
    pass

class StatusVeiculo(Enum):
    ATIVO = "Ativo"
    MANUTENCAO = "Em Manutenção"
    INATIVO = "Inativo"

class EstrategiaManutencao(ABC):
    @abstractmethod
    def calcular_custo(self, valor_base: float) -> float:
        pass

class ManutencaoBasica(EstrategiaManutencao):
    def calcular_custo(self, valor_base: float) -> float:
        return valor_base

class ManutencaoCorretiva(EstrategiaManutencao):
    def calcular_custo(self, valor_base: float) -> float:
        return valor_base * 1.20

class Manutencao:
    def __init__(self, data: str, tipo: str, custo_base: float, descricao: str):
        self.data = data
        self.tipo = tipo
        self.descricao = descricao
        self.custo_base = float(custo_base)
        
        if self.tipo.lower() == "corretiva":
            self.estrategia = ManutencaoCorretiva()
        else:
            self.estrategia = ManutencaoBasica()
            
        self.custo_final = self.estrategia.calcular_custo(self.custo_base)

    def to_dict(self):
        return {
            "data": self.data,
            "tipo": self.tipo,
            "custo_base": self.custo_base,
            "custo_final": self.custo_final,
            "descricao": self.descricao
        }

class Abastecimento:
    def __init__(self, data: str, combustivel: str, litros: float, valor: float):
        self.data = data
        self.combustivel = combustivel
        self.litros = float(litros)
        self.valor = float(valor)

    def to_dict(self):
        return {
            "data": self.data,
            "combustivel": self.combustivel,
            "litros": self.litros,
            "valor": self.valor
        }

class ManutenivelMixin:
    def registrar_manutencao_status(self):
        if self.status != StatusVeiculo.ATIVO:
             raise ManutencaoInvalidaError(f"Veículo já está {self.status.value}")
        self.status = StatusVeiculo.MANUTENCAO
    
    def finalizar_manutencao_status(self):
        if self.status == StatusVeiculo.MANUTENCAO:
            self.status = StatusVeiculo.ATIVO
        else:
            raise ManutencaoInvalidaError("Veículo não está em manutenção.")

class AbastecivelMixin:
    def abastecer(self, abastecimento: Abastecimento):
        self.historico_abastecimentos.append(abastecimento)

class Pessoa:
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.__cpf = cpf

    @property
    def cpf(self) -> str:
        return self.__cpf

    def to_dict(self):
        return {"nome": self.nome, "cpf": self.cpf}

class Motorista(Pessoa):
    def __init__(self, nome: str, cpf: str, cnh: str, categoria_cnh: str):
        super().__init__(nome, cpf)
        self.cnh = cnh
        self.categoria_cnh = categoria_cnh.upper()

    def to_dict(self):
        data = super().to_dict()
        data.update({"cnh": self.cnh, "categoria_cnh": self.categoria_cnh})
        return data
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['nome'], data['cpf'], data['cnh'], data['categoria_cnh'])

    def __str__(self):
        return f"{self.nome} | CPF: {self.cpf} | CNH: {self.categoria_cnh}"

class Veiculo(ABC, ManutenivelMixin, AbastecivelMixin):
    def __init__(self, placa: str, marca: str, modelo: str, ano: int, km_inicial: float = 0, status: str = "Ativo"):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.ano = int(ano)
        
        self.__quilometragem = float(km_inicial)
        self.km_entrada = float(km_inicial) 
        
        self.historico_manutencoes: List[Manutencao] = []
        self.historico_abastecimentos: List[Abastecimento] = []

        if isinstance(status, str):
            self.__status = StatusVeiculo(status)
        else:
            self.__status = status

    @property
    def quilometragem(self) -> float:
        return self.__quilometragem

    @quilometragem.setter
    def quilometragem(self, nova_km: float):
        if nova_km < self.__quilometragem:
            raise ValueError("A quilometragem não pode ser reduzida.")
        self.__quilometragem = nova_km

    @property
    def status(self) -> StatusVeiculo:
        return self.__status

    @status.setter
    def status(self, novo_status: StatusVeiculo):
        self.__status = novo_status

    def adicionar_manutencao(self, manutencao: Manutencao):
        self.registrar_manutencao_status()
        self.historico_manutencoes.append(manutencao)

    def __lt__(self, other):
        if not isinstance(other, Veiculo): return NotImplemented
        return self.quilometragem < other.quilometragem

    def __iter__(self):
        return iter(self.historico_manutencoes)

    def __str__(self):
        return f"[{self.placa}] {self.modelo} ({self.marca}) - {self.status.value}"

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "placa": self.placa,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "quilometragem": self.quilometragem,
            "km_entrada": self.km_entrada,
            "status": self.status.value,
            "manutencoes": [m.to_dict() for m in self.historico_manutencoes],
            "abastecimentos": [a.to_dict() for a in self.historico_abastecimentos]
        }
    
    @classmethod
    def from_dict(cls, data):
        tipo = data.get('tipo', 'Carro')
        status = data.get('status', 'Ativo')
        
        if tipo == "Carro": classe = Carro
        elif tipo == "Moto": classe = Moto
        elif tipo in ["Caminhão", "Caminhao"]: classe = Caminhao
        else: classe = Carro
            
        veiculo = classe(
            data['placa'], data['marca'], data['modelo'], 
            data['ano'], data['quilometragem'], status
        )
        
        veiculo.km_entrada = data.get('km_entrada', veiculo.quilometragem)
        
        for m in data.get('manutencoes', []):
            manut = Manutencao(m['data'], m['tipo'], m['custo_base'], m.get('descricao', ''))
            manut.custo_final = m.get('custo_final', m['custo_base']) 
            veiculo.historico_manutencoes.append(manut)

        for a in data.get('abastecimentos', []):
            abast = Abastecimento(a['data'], a['combustivel'], a['litros'], a['valor'])
            veiculo.historico_abastecimentos.append(abast)
            
        return veiculo

class Carro(Veiculo):
    tipo = "Carro"
    categoria_minima_cnh = "B"

class Moto(Veiculo):
    tipo = "Moto"
    categoria_minima_cnh = "A"

class Caminhao(Veiculo):
    tipo = "Caminhão"
    categoria_minima_cnh = "C"

class Viagem:
    def __init__(self, motorista: Motorista, veiculo: Veiculo, destino: str, distancia: float):
        self.motorista = motorista
        self.veiculo = veiculo
        self.destino = destino
        self.distancia = float(distancia)
        self._validar_alocacao()

    def _validar_alocacao(self):
        if self.veiculo.status != StatusVeiculo.ATIVO:
            raise AlocacaoInvalidaError(f"Veículo {self.veiculo.placa} está {self.veiculo.status.value}")

        req = self.veiculo.categoria_minima_cnh
        cnh_mot = self.motorista.categoria_cnh
        
        compativel = False
        if req in cnh_mot: compativel = True
        if req == "B" and any(cat in cnh_mot for cat in ["C", "D", "E"]): compativel = True
        if req == "C" and any(cat in cnh_mot for cat in ["D", "E"]): compativel = True

        if not compativel:
            raise AlocacaoInvalidaError(f"CNH {cnh_mot} incompatível com {self.veiculo.tipo} (Req: {req})")

    def realizar_viagem(self):
        nova_km = self.veiculo.quilometragem + self.distancia
        self.veiculo.quilometragem = nova_km

    def to_dict(self):
        return {
            "cpf_motorista": self.motorista.cpf,
            "nome_motorista": self.motorista.nome,
            "placa_veiculo": self.veiculo.placa,
            "modelo_veiculo": self.veiculo.modelo,
            "destino": self.destino,
            "distancia": self.distancia
        }