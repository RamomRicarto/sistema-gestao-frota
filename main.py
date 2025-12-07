import controller
import views
from models import AlocacaoInvalidaError, ManutencaoInvalidaError

def main():
    while True:
        views.exibir_cabecalho()
        print("1.  Listar Frota")
        print("2.  Cadastrar Veículo")  
        print("3.  Cadastrar Motorista")  
        print("4.  Registrar Viagem (Alocação)")
        print("5.  Registrar Manutenção")
        print("6.  Finalizar Manutenção")
        print("0.  Sair")
        
        opcao = input("Escolha uma opção: ")

        try:
            if opcao == "1":
                veiculos = controller.carregar_veiculos()
                views.exibir_relatorio_frota([v.to_dict() for v in veiculos])
            
            elif opcao == "2":
                print("\n--- Novo Veículo ---")
                tipo = input("Tipo (Carro/Moto/Caminhao): ")
                placa = input("Placa: ")
                marca = input("Marca: ")
                modelo = input("Modelo: ")
                ano = input("Ano: ")
                km = input("KM Inicial: ")
                
                msg = controller.cadastrar_veiculo_controller(tipo, placa, marca, modelo, ano, km)
                print(f"OK: {msg}")

            elif opcao == "3":
                print("\n--- Novo Motorista ---")
                nome = input("Nome: ")
                cpf = input("CPF: ")
                cnh = input("Nº CNH: ")
                cat = input("Categoria CNH (A, B, C, AB...): ")

                msg = controller.cadastrar_motorista_controller(nome, cpf, cnh, cat)
                print(f"OK: {msg}")
            
            elif opcao == "4":
                print("\n--- Nova Viagem ---")
                cpf = input("CPF do Motorista: ")
                placa = input("Placa do Veículo: ")
                destino = input("Destino: ")
                dist = input("Distância (km): ")
                msg = controller.realizar_viagem_controller(cpf, placa, destino, dist)
                print(f"OK: {msg}")

            elif opcao == "5":
                placa = input("Placa do Veículo para Manutenção: ")
                msg = controller.realizar_manutencao_controller(placa)
                print(f"MANUTENÇÃO: {msg}")

            elif opcao == "6":
                placa = input("Placa do Veículo para Liberar: ")
                msg = controller.finalizar_manutencao_controller(placa)
                print(f"OK: {msg}")

            elif opcao == "0":
                print("Encerrando sistema...")
                break
            
            else:
                print("Opção inválida!")

        except (AlocacaoInvalidaError, ManutencaoInvalidaError) as e:
            print(f"ERRO DE REGRA DE NEGÓCIO: {e}")
        except Exception as e:
            print(f"ERRO: {e}")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
