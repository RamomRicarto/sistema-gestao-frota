class Pessoa:
    """
    Entidade base representando uma pessoa física (Nome, CPF).
    """
    pass

class Motorista(Pessoa):
    """
    Condutor habilitado responsável por realizar as viagens.
    """
    pass

class Veiculo:
    """
    Base para veículos da frota com controle de manutenção e quilometragem.
    """
    pass

class Carro(Veiculo):
    """
    Veículo de passeio ou carga leve.
    """
    pass

class Moto(Veiculo):
    """
    Veículo ágil para pequenas cargas ou deslocamento rápido.
    """
    pass

class Caminhao(Veiculo):
    """
    Veículo pesado destinado ao transporte de grandes cargas.
    """
    pass

class Viagem:
    """
    Registra a operação de transporte vinculando Motorista e Veículo.
    """
    pass