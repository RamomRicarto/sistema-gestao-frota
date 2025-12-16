import pytest
from models import (
    Carro, Moto, Motorista, StatusVeiculo, 
    Manutencao, ManutencaoInvalidaError, AlocacaoInvalidaError, Viagem
)

def test_criar_veiculo():
    carro = Carro("ABC-1234", "Fiat", "Uno", 2020, 10000)
    assert carro.placa == "ABC-1234"
    assert carro.quilometragem == 10000.0
    assert carro.status == StatusVeiculo.ATIVO

def test_criar_motorista():
    mot = Motorista("João", "123.456.789-00", "CNH123", "B")
    assert mot.categoria_cnh == "B"
    assert mot.nome == "João"

def test_nao_diminuir_km():
    caminhao = Carro("TST-0001", "Volvo", "FH", 2021, 50000)
    with pytest.raises(ValueError) as erro:
        caminhao.quilometragem = 20000
    assert "não pode ser reduzida" in str(erro.value)

def test_strategy_manutencao_preventiva():
    m = Manutencao("01/01/2025", "Preventiva", 100.0, "Troca de óleo")
    assert m.custo_final == 100.0

def test_strategy_manutencao_corretiva():
    m = Manutencao("01/01/2025", "Corretiva", 100.0, "Motor fundido")
    assert m.custo_final == 120.0

def test_fluxo_manutencao():
    moto = Moto("MTO-9999", "Honda", "CG", 2022, 1000)
    manut = Manutencao("01/01", "Preventiva", 50, "Revisão")
    
    moto.adicionar_manutencao(manut)
    assert moto.status == StatusVeiculo.MANUTENCAO
    
    with pytest.raises(ManutencaoInvalidaError):
        moto.adicionar_manutencao(manut)
        
    moto.finalizar_manutencao_status()
    assert moto.status == StatusVeiculo.ATIVO

def test_ordenacao_veiculos_magic_method():
    v1 = Carro("A", "M", "M", 2020, 100)
    v2 = Carro("B", "M", "M", 2020, 200)
    assert v1 < v2 

def test_iteracao_historico_magic_method():
    carro = Carro("ITR-000", "M", "M", 2020)
    m1 = Manutencao("D1", "P", 100, "D1")
    m2 = Manutencao("D2", "P", 200, "D2")
    
   
    carro.historico_manutencoes.append(m1)
    carro.historico_manutencoes.append(m2)
    
  
    custo_total = sum(m.custo_final for m in carro)
    assert custo_total == 300.0

def test_viagem_compatibilidade_cnh():
    mot = Motorista("Ana", "111", "123", "B") 
    moto = Moto("MOTO", "H", "H", 2020)       
    
    with pytest.raises(AlocacaoInvalidaError):
        Viagem(mot, moto, "Destino", 100)

def test_viagem_veiculo_manutencao():
    mot = Motorista("Ana", "111", "123", "B")
    carro = Carro("CAR", "F", "F", 2020, status="Em Manutenção")
    
    with pytest.raises(AlocacaoInvalidaError):
        Viagem(mot, carro, "Destino", 100)