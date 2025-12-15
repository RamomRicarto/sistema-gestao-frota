import pytest
import os
import shutil
import controller
from models import StatusVeiculo, AlocacaoInvalidaError

@pytest.fixture(autouse=True)
def setup_test_environment():
    TEST_DIR = "data_test"
    
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    controller.DATA_DIR = TEST_DIR
    controller.FILE_VEICULOS = os.path.join(TEST_DIR, "veiculos.json")
    controller.FILE_MOTORISTAS = os.path.join(TEST_DIR, "motoristas.json")
    controller.FILE_VIAGENS = os.path.join(TEST_DIR, "viagens.json")
    
    yield
    
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)


def test_fluxo_cadastro_e_edicao_veiculo():
    """Testa cadastrar um carro, verificar se salvou e depois editar."""
    msg = controller.cadastrar_veiculo_controller("Carro", "ABC-1000", "Fiat", "Uno", "2020", "10000")
    assert "sucesso" in msg.lower()

    veiculo = controller.buscar_veiculo("ABC-1000")
    assert veiculo is not None
    assert veiculo.modelo == "Uno"
    
    controller.atualizar_veiculo_controller("ABC-1000", "Fiat", "Mille", "2021")
    
    veiculo_atualizado = controller.buscar_veiculo("ABC-1000")
    assert veiculo_atualizado.modelo == "Mille"
    assert veiculo_atualizado.ano == 2021

def test_fluxo_cadastro_motorista():
    """Testa cadastrar motorista e verificar persistência."""
    controller.cadastrar_motorista_controller("João Teste", "111.222.333-44", "CNH123", "B")
    
    mot = controller.buscar_motorista("111.222.333-44")
    assert mot is not None
    assert mot.categoria_cnh == "B"


def test_fluxo_viagem_com_sucesso():
    """Cadastra motorista e veiculo compatíveis e realiza viagem."""
    controller.cadastrar_veiculo_controller("Carro", "CAR-01", "Ford", "Ka", "2022", "5000")
    controller.cadastrar_motorista_controller("Maria", "999.888.777-66", "CNH999", "B")
    
    msg = controller.realizar_viagem_controller("999.888.777-66", "CAR-01", "Praia", "100")
    
    assert "registrada" in msg.lower()
    
    veiculo = controller.buscar_veiculo("CAR-01")
    assert veiculo.quilometragem == 5100.0  
def test_bloqueio_viagem_categoria_incompativel():
    """Motorista B tentando dirigir Caminhão C."""
    controller.cadastrar_veiculo_controller("Caminhão", "CAM-01", "Volvo", "FH", "2020", "10000")
    controller.cadastrar_motorista_controller("Pedro", "111.111.111-11", "CNH111", "B")
    
    with pytest.raises(Exception) as excinfo:
        controller.realizar_viagem_controller("111.111.111-11", "CAM-01", "Entrega", "500")
    
    assert "CNH" in str(excinfo.value)

def test_fluxo_manutencao_completo_strategy():
    """
    Testa:
    1. Registrar manutenção (Corretiva -> Taxa extra).
    2. Verificar status do veículo (Em Manutenção).
    3. Tentar viajar (Deve falhar).
    4. Finalizar manutenção.
    5. Verificar status (Ativo).
    """
    controller.cadastrar_veiculo_controller("Moto", "MTO-01", "Honda", "CG", "2021", "2000")
    
    msg = controller.registrar_manutencao_controller("MTO-01", "01/01/2025", "Corretiva", "100", "Pneu furado")
    assert "120.00" in msg 
    veiculo = controller.buscar_veiculo("MTO-01")
    assert veiculo.status == StatusVeiculo.MANUTENCAO
    
    controller.cadastrar_motorista_controller("Motoqueiro", "222", "CNH222", "A")
    with pytest.raises(Exception) as exc:
        controller.realizar_viagem_controller("222", "MTO-01", "Rua A", "10")
    assert "Manutenção" in str(exc.value) or "está Em Manutenção" in str(exc.value)
    
    controller.finalizar_manutencao_controller("MTO-01")
    
    veiculo = controller.buscar_veiculo("MTO-01")
    assert veiculo.status == StatusVeiculo.ATIVO

def test_registro_abastecimento_e_eficiencia():
    """Testa registrar abastecimento e verificar cálculo de eficiência."""
    controller.cadastrar_veiculo_controller("Carro", "ECO-01", "Fiat", "Mobi", "2023", "1000")
    
    controller.registrar_abastecimento_controller("ECO-01", "01/01/2025", "Gasolina", "50", "250")
    
    relatorio = controller.gerar_relatorio_eficiencia()
    
    dados_carro = next(d for d in relatorio if d['placa'] == "ECO-01")
    assert dados_carro['km_l'] == 20.0


def test_geracao_relatorios_nao_quebra():
    """Garante que chamar os relatórios sem dados ou com dados não gera erro."""
    assert controller.gerar_relatorio_custos() == []
    assert controller.gerar_relatorio_eficiencia() == []
    
    controller.cadastrar_veiculo_controller("Carro", "REL-01", "X", "Y", "2020", "0")
    assert len(controller.gerar_relatorio_custos()) == 1