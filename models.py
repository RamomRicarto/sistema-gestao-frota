from enum import Enum
from abc import ABC, abstractmethod

class AlocacaoInvalidaError(Exception):
    pass

class ManutencaoInvalidaError(Exception):
    pass

class StatusVeiculo(Enum):
    ATIVO = "Ativo"
    MANUTENCAO = "Em Manutenção"
    INATIVO = "Inativo"

class ManutenivelMixin:
    def registrar_manutencao(self):
        if self.status != StatusVeiculo.ATIVO:
             raise ManutencaoInvalidaError(f"Veículo já está {self.status.value}")
        self.status = StatusVeiculo.MANUTENCAO
    
    def finalizar_manutencao(self):
        if self.status == StatusVeiculo.MANUTENCAO:
            self.status = StatusVeiculo.ATIVO

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
        self.__cnh = cnh
        self.categoria_cnh = categoria_cnh.upper()

    @property
    def cnh(self) -> str:
        return self.__cnh

    def to_dict(self):
        data = super().to_dict()
        data.update({"cnh": self.cnh, "categoria_cnh": self.categoria_cnh})
        return data
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['nome'], data['cpf'], data['cnh'], data['categoria_cnh'])

    def __str__(self):
        return f"{self.nome} (CNH: {self.categoria_cnh})"

class Veiculo(ABC, ManutenivelMixin):
    def __init__(self, placa: str, marca: str, modelo: str, ano: int, km_inicial: float = 0, status: str = "Ativo"):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.__quilometragem = km_inicial

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

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "placa": self.placa,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "quilometragem": self.quilometragem,
            "status": self.status.value
        }
    
    @classmethod
    def from_dict(cls, data):
        """Recria o veículo correto com base no dicionário."""
        tipo = data.get('tipo')
        status = data.get('status', 'Ativo')
        
        if tipo == "Carro":
            classe = Carro
        elif tipo == "Moto":
            classe = Moto
        elif tipo == "Caminhão":
            classe = Caminhao
        else:
            classe = Carro
            
        return classe(
            data['placa'], data['marca'], data['modelo'], 
            data['ano'], data['quilometragem'], status
        )

    def __str__(self):
        return f"[{self.placa}] {self.modelo} - {self.status.value}"

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
        self.distancia = distancia
        
        self._validar_alocacao()

    def _validar_alocacao(self):
        if self.veiculo.status != StatusVeiculo.ATIVO:
            raise AlocacaoInvalidaError(
                f"Veículo {self.veiculo.placa} está {self.veiculo.status.value}"
            )

        req_veiculo = self.veiculo.categoria_minima_cnh
        cnh_motorista = self.motorista.categoria_cnh

        regras_permitidas = {
            'A': ['A'],                # A só dirige A
            'B': ['B'],                # Min B -> aceita B
            'C': ['B', 'C'],           # Min C -> aceita B ou C
            'D': ['B', 'C', 'D'],      # Min D -> aceita B, C ou D
            'E': ['B', 'C', 'D', 'E']  # Min E -> aceita B, C, D ou E
        }

        letras_aceitas = regras_permitidas.get(req_veiculo, [])

        tem_permissao = any(letra in cnh_motorista for letra in letras_aceitas)

        if not tem_permissao:
            raise AlocacaoInvalidaError(
                f"Motorista CNH {cnh_motorista} não pode dirigir {self.veiculo.tipo}. "
                f"O veículo exige categoria '{req_veiculo}', que nesta regra aceita CNHs contendo: {letras_aceitas}"
            )

    def realizar_viagem(self):
        """Atualiza a quilometragem do veículo somando a distância da viagem."""
        nova_km = self.veiculo.quilometragem + self.distancia
        self.veiculo.quilometragem = nova_km
        print(f"Viagem para {self.destino} finalizada. Nova KM do veículo: {self.veiculo.quilometragem}")

    def to_dict(self):
        return {
            "cpf_motorista": self.motorista.cpf,
            "placa_veiculo": self.veiculo.placa,
            "destino": self.destino,
            "distancia": self.distancia
        }

    def __str__(self):
        return f"Viagem de {self.motorista.nome} para {self.destino} com {self.veiculo.modelo}"
