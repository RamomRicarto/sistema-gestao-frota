from enum import Enum
from abc import ABC

class StatusVeiculo(Enum):
    ATIVO = "Ativo"
    MANUTENCAO = "Em Manutenção"
    INATIVO = "Inativo"

class Pessoa:
    """Entidade base representando uma pessoa física."""
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.__cpf = cpf

    @property
    def cpf(self) -> str:
        return self.__cpf

    def to_dict(self):
        """Converte dados básicos para dicionário."""
        return {"nome": self.nome, "cpf": self.cpf}

class Motorista(Pessoa):
    """Condutor habilitado responsável por realizar as viagens."""
    def __init__(self, nome: str, cpf: str, cnh: str, categoria_cnh: str):
        super().__init__(nome, cpf)
        self.__cnh = cnh
        self.categoria_cnh = categoria_cnh.upper()

    @property
    def cnh(self) -> str:
        return self.__cnh

    def to_dict(self):
        """Inclui dados da CNH no dicionário."""
        data = super().to_dict()
        data.update({"cnh": self.cnh, "categoria_cnh": self.categoria_cnh})
        return data

    def __str__(self):
        return f"{self.nome} (CNH: {self.categoria_cnh})"

class Veiculo(ABC):
    """Base para veículos da frota."""
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
        if nova_km < self.__quilometragem:
            raise ValueError("A quilometragem não pode ser reduzida.")
        self.__quilometragem = nova_km

    @property
    def status(self) -> StatusVeiculo:
        return self.__status

    @status.setter
    def status(self, novo_status: StatusVeiculo):
        self.__status = novo_status

    def to_dict(self):
        """Converte veículo para dicionário para salvar no JSON."""
        return {
            "tipo": self.__class__.__name__, # Salva se é Carro, Moto ou Caminhao
            "placa": self.placa,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "quilometragem": self.quilometragem,
            "status": self.status.value
        }

    def __str__(self):
        return f"[{self.placa}] {self.marca} {self.modelo} - {self.status.value}"

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
    """
    Classe de Relacionamento: Vincula um Motorista a um Veículo.
    """
    def __init__(self, motorista: Motorista, veiculo: Veiculo, destino: str, distancia: float):
        self.motorista = motorista
        self.veiculo = veiculo
        self.destino = destino
        self.distancia = distancia

    def realizar_viagem(self):
        """Atualiza a quilometragem do veículo ao fechar a viagem."""
        nova_km = self.veiculo.quilometragem + self.distancia
        self.veiculo.quilometragem = nova_km

    def to_dict(self):
        """Salva o relacionamento (apenas identificadores principais)."""
        return {
            "cpf_motorista": self.motorista.cpf,
            "placa_veiculo": self.veiculo.placa,
            "destino": self.destino,
            "distancia": self.distancia
        }
    
    def __str__(self):
        return f"Viagem para {self.destino} ({self.distancia}km) | Condutor: {self.motorista.nome} -> Veículo: {self.veiculo.modelo}"