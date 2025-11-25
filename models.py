from enum import Enum
from abc import ABC

class StatusVeiculo(Enum):
    ATIVO = "Ativo"
    MANUTENCAO = "Em Manutenção"
    INATIVO = "Inativo"

class Pessoa:
    """
    Entidade base representando uma pessoa física (Nome, CPF).
    """
    
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.__cpf = cpf

    @property
    def cpf(self) -> str:
        return self.__cpf
    
    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"

class Motorista(Pessoa):
    """
    Condutor habilitado responsável por realizar as viagens.
    """
    
    def __init__(self, nome: str, cpf: str, cnh: str, categoria_cnh: str):
        super().__init__(nome, cpf)
        self.__cnh = cnh
        self.categoria_cnh = categoria_cnh.upper()

    @property
    def cnh(self) -> str:
        return self.__cnh

    def __str__(self):
        return f"Mot. {self.nome} - CNH {self.categoria_cnh}"

class Veiculo(ABC):
    """
    Base para veículos da frota com controle de manutenção e quilometragem.
    """
    def __init__(self, placa: str, marca: str, modelo: str, ano: int, km_inicial: float = 0):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        
        self.__quilometragem = km_inicial
        self.__status = StatusVeiculo.ATIVO

    @property
    def quilometragem(self) -> float:
        return self.__quilometragem

    @quilometragem.setter
    def quilometragem(self, nova_km: float):
        if nova_km < 0:
            raise ValueError("A quilometragem não pode ser negativa.")
        if nova_km < self.__quilometragem:
            raise ValueError("A quilometragem não pode ser reduzida.")
        self.__quilometragem = nova_km

    @property
    def status(self) -> StatusVeiculo:
        return self.__status

    @status.setter
    def status(self, novo_status: StatusVeiculo):
        if not isinstance(novo_status, StatusVeiculo):
            raise ValueError("Status inválido.")
        self.__status = novo_status

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa}) - {self.status.value}"

    def __eq__(self, outro_veiculo):
        if isinstance(outro_veiculo, Veiculo):
            return self.placa == outro_veiculo.placa
        return False

class Carro(Veiculo):
    """Veículo de passeio ou carga leve."""
    tipo = "Carro"
    categoria_minima_cnh = "B"

class Moto(Veiculo):
    """Veículo ágil para pequenas cargas ou deslocamento rápido."""
    tipo = "Moto"
    categoria_minima_cnh = "A"

class Caminhao(Veiculo):
    """Veículo pesado destinado ao transporte de grandes cargas."""
    tipo = "Caminhão"
    categoria_minima_cnh = "C"

class Viagem:
    """
    Registra a operação de transporte vinculando Motorista e Veículo.
    """
    pass