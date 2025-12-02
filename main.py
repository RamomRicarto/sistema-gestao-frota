from models import Carro, Caminhao, Motorista, Viagem
import controller
import views

def main():
    views.exibir_cabecalho()

    carro1 = Carro("ABC-1234", "Toyota", "Corolla", 2022, km_inicial=15000)
    caminhao1 = Caminhao("XYZ-9090", "Volvo", "FH 540", 2020, km_inicial=120000)
    frota = [carro1, caminhao1]

    mot1 = Motorista("João Silva", "111.222.333-00", "123456789", "C")
    motoristas = [mot1]

    viagem1 = Viagem(motorista=mot1, veiculo=caminhao1, destino="São Paulo", distancia=500.5)
    viagem1.realizar_viagem()
    viagens = [viagem1]

    views.exibir_inicio_salvamento()
    
    controller.salvar_dados(frota, controller.FILE_VEICULOS)
    views.exibir_mensagem_salvamento(controller.FILE_VEICULOS)

    controller.salvar_dados(motoristas, controller.FILE_MOTORISTAS)
    views.exibir_mensagem_salvamento(controller.FILE_MOTORISTAS)

    controller.salvar_dados(viagens, controller.FILE_VIAGENS)
    views.exibir_mensagem_salvamento(controller.FILE_VIAGENS)

    # 4. Relatórios (Controller busca dados -> View exibe)
    dados_frota_disco = controller.carregar_dados_veiculos()
    views.exibir_relatorio_frota(dados_frota_disco)
    
    views.exibir_relatorio_viagens(viagens)

if __name__ == "__main__":
    main()
