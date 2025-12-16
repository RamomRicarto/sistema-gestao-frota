import controller
import views
from models import AlocacaoInvalidaError, ManutencaoInvalidaError

def main():
    while True:
        views.exibir_cabecalho()
        print("--- GESTÃO DE CADASTROS ---")
        print("1.  Listar Frota Completa")
        print("2.  Cadastrar Veículo")
        print("3.  Cadastrar Motorista")
        print("4.  Buscar/Detalhar Veículo")
        print("5.  Buscar/Detalhar Motorista")
        print("6.  Editar Veículo")
        print("7.  Editar Motorista")
        print("\n--- OPERAÇÕES DIÁRIAS ---")
        print("8.  Registrar Viagem (Alocação)")
        print("9.  Registrar Abastecimento")
        print("10. Registrar Manutenção")
        print("11. Finalizar Manutenção (Liberar Veículo)")
        print("\n--- RELATÓRIOS GERENCIAIS ---")
        print("12. Relatório de Custos Manutenção")
        print("13. Ranking de Eficiência (Km/l)")
        print("0.  Sair")
        
        opcao = input("\nEscolha uma opção: ")

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
                print(f"SUCESSO: {msg}")

            elif opcao == "3":
                print("\n--- Novo Motorista ---")
                nome = input("Nome: ")
                cpf = input("CPF: ")
                cnh = input("CNH: ")
                cat = input("Categoria CNH: ")
                msg = controller.cadastrar_motorista_controller(nome, cpf, cnh, cat)
                print(f"SUCESSO: {msg}")

            elif opcao == "4":
                placa = input("Digite a Placa: ")
                v = controller.buscar_veiculo(placa)
                if v: views.exibir_detalhes_veiculo(v)
                else: print("Veículo não encontrado.")

            elif opcao == "5":
                cpf = input("Digite o CPF: ")
                m = controller.buscar_motorista(cpf)
                if m: views.exibir_detalhes_motorista(m)
                else: print("Motorista não encontrado.")

            elif opcao == "6":
                placa = input("Placa do veículo a editar: ")
                print("(Deixe em branco para manter o valor atual)")
                marca = input("Nova Marca: ")
                modelo = input("Novo Modelo: ")
                ano = input("Novo Ano: ")
                msg = controller.atualizar_veiculo_controller(placa, marca, modelo, ano)
                print(f"RESULTADO: {msg}")

            elif opcao == "7":
                cpf = input("CPF do motorista a editar: ")
                print("(Deixe em branco para manter o valor atual)")
                nome = input("Novo Nome: ")
                cnh = input("Nova CNH: ")
                cat = input("Nova Categoria: ")
                msg = controller.atualizar_motorista_controller(cpf, nome, cnh, cat)
                print(f"RESULTADO: {msg}")

            elif opcao == "8":
                cpf = input("CPF Motorista: ")
                placa = input("Placa Veículo: ")
                dest = input("Destino: ")
                dist = input("Distância (km): ")
                msg = controller.realizar_viagem_controller(cpf, placa, dest, dist)
                print(f"SUCESSO: {msg}")

            elif opcao == "9":
                placa = input("Placa Veículo: ")
                data = input("Data (DD/MM/AAAA): ")
                comb = input("Combustível: ")
                litros = input("Litros: ")
                valor = input("Valor Total (R$): ")
                msg = controller.registrar_abastecimento_controller(placa, data, comb, litros, valor)
                print(f"SUCESSO: {msg}")

            elif opcao == "10":
                placa = input("Placa Veículo: ")
                data = input("Data: ")
                tipo = input("Tipo (Preventiva/Corretiva): ")
                custo = input("Custo Base (R$): ")
                desc = input("Descrição: ")
                msg = controller.registrar_manutencao_controller(placa, data, tipo, custo, desc)
                print(f"SUCESSO: {msg}")

            elif opcao == "11":
                placa = input("Placa Veículo para liberar: ")
                msg = controller.finalizar_manutencao_controller(placa)
                print(f"SUCESSO: {msg}")
            
            elif opcao == "12":
                dados = controller.gerar_relatorio_custos()
                views.exibir_relatorio_custos(dados)

            elif opcao == "13":
                dados = controller.gerar_relatorio_eficiencia()
                views.exibir_ranking_eficiencia(dados)

            elif opcao == "0":
                print("Encerrando sistema...")
                break
            else:
                print("Opção inválida!")

        except (AlocacaoInvalidaError, ManutencaoInvalidaError) as e:
            print(f"\n[ERRO DE REGRA DE NEGÓCIO]: {e}")
        except Exception as e:
            print(f"\n[ERRO]: {e}")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()