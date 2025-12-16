from typing import List, Dict, Any

def exibir_cabecalho():
    print("\n" + "="*40)
    print("=== SISTEMA DE GESTÃO DE FROTA v1.0 ===")
    print("="*40 + "\n")

def exibir_detalhes_veiculo(v):
    print(f"\n--- Detalhes do Veículo [{v.placa}] ---")
    print(f"Modelo/Marca: {v.modelo} / {v.marca}")
    print(f"Tipo: {v.tipo}")
    print(f"Ano: {v.ano}")
    print(f"KM Atual: {v.quilometragem}")
    print(f"Status: {v.status.value}")
    print(f"Histórico Manutenções: {len(v.historico_manutencoes)} registros")
    print(f"Histórico Abastecimentos: {len(v.historico_abastecimentos)} registros")

def exibir_detalhes_motorista(m):
    print(f"\n--- Detalhes do Motorista ---")
    print(f"Nome: {m.nome}")
    print(f"CPF: {m.cpf}")
    print(f"CNH: {m.cnh} (Categoria: {m.categoria_cnh})")

def exibir_relatorio_frota(dados_veiculos: List[Dict[str, Any]]):
    print("\n--- Relatório Geral da Frota ---")
    if not dados_veiculos:
        print("Nenhum veículo cadastrado.")
        return

    print(f"{'PLACA':<10} | {'MODELO':<15} | {'STATUS':<15} | {'KM':<10}")
    print("-" * 60)
    for item in dados_veiculos:
        placa = item.get('placa', '---')
        modelo = item.get('modelo', '---')
        status = item.get('status', '---')
        km = item.get('quilometragem', 0)
        print(f"{placa:<10} | {modelo:<15} | {status:<15} | {km:<10}")

def exibir_relatorio_custos(dados: List[Dict]):
    print("\n--- Relatório de Custos de Manutenção ---")
    if not dados:
        print("Sem dados.")
        return
    
    print(f"{'PLACA':<10} | {'QTD':<5} | {'CUSTO TOTAL'}")
    print("-" * 40)
    for d in dados:
        print(f"{d['placa']:<10} | {d['qtd_manutencoes']:<5} | R$ {d['total_manutencao']:.2f}")

def exibir_ranking_eficiencia(dados: List[Dict]):
    print("\n--- Ranking de Eficiência (Combustível) ---")
    if not dados:
        print("Sem dados.")
        return

    print(f"{'POS':<3} | {'PLACA':<10} | {'MODELO':<15} | {'KM/L':<10}")
    print("-" * 50)
    for i, d in enumerate(dados, 1):
        print(f"{i:<3} | {d['placa']:<10} | {d['modelo']:<15} | {d['km_l']:.2f} km/l")