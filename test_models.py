import pytest
from models import Carro, Moto, Motorista, StatusVeiculo

def test_criar_veiculo():
    carro = Carro("ABC-1234", "marca", "modelo", 2020, 10000)
    
    assert carro.placa == "ABC-1234"
    assert carro.quilometragem == 10000
    assert carro.status == StatusVeiculo.ATIVO

def test_atualizar_km():
    moto = Moto("XYZ-9999", "marca moto", "modelo moto", 2022, 5000)
    
    moto.quilometragem = 5100 
    
    assert moto.quilometragem == 5100

def test_nao_diminuir_km():
    caminhao = Carro("TST-0001", "marca caminhao", "modelo", 2021, 50000)
    
    with pytest.raises(ValueError) as erro:
        caminhao.quilometragem = 20000
    
    assert "não pode ser reduzida" in str(erro.value)

def test_criar_motorista_heranca():
    mot = Motorista("ramom", "111.222.333-44", "12345678900", "AD")
    
    assert mot.nome == "ramom"
    assert mot.cpf == "111.222.333-44"
    
    assert mot.cnh == "12345678900"
    assert mot.categoria_cnh == "AD"

def test_veiculos_placa_igual():
    v1 = Carro("ABC-1234", "marca 1", "mod 1", 2020)
    v2 = Carro("ABC-1234", "marca 2", "mod 2", 2022) 
    
    assert v1 == v2