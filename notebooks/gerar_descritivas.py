import pandas as pd
import numpy as np

def calcular_estatisticas_descritivas(caminho_csv: str):
    """
    Calcula e imprime estatísticas descritivas de colunas chave
    do arquivo IC_Dados_Processados.csv.
    """
    try:
        df = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        print(f"ERRO: O arquivo {caminho_csv} não foi encontrado.")
        print("Certifique-se de que o script run_pipeline.py foi executado e gerou o arquivo.")
        return

    print("--- Estatísticas Descritivas ---")
    print(f"Número total de participantes: {len(df)}")

    # Idade
    if 'IDADE' in df.columns:
        print("\n--- IDADE ---")
        print(f"Média de Idade: {df['IDADE'].mean():.2f} anos")
        print(f"Desvio Padrão da Idade: {df['IDADE'].std():.2f} anos")
        print(f"Mínimo de Idade: {df['IDADE'].min()} anos")
        print(f"Máximo de Idade: {df['IDADE'].max()} anos")
    else:
        print("\nAVISO: Coluna 'IDADE' não encontrada.")

    # Gênero (usando GENERO_COD e assumindo o mapeamento padrão, idealmente teríamos a coluna original)
    # Mapeamento reverso (parcial, baseado no que foi visto no script de processamento)
    # O ideal seria ter GENERO_TEXTO no CSV processado ou o mapeamento completo.
    # Estou assumindo: {1: 'Masculino', 2: 'Feminino', 3: 'Prefiro não responder', 4: 'Não-binário'}
    if 'GENERO_COD' in df.columns:
        print("\n--- GÊNERO (baseado em GENERO_COD) ---")
        genero_counts = df['GENERO_COD'].value_counts()
        genero_percent = df['GENERO_COD'].value_counts(normalize=True) * 100
        print(f"Masculino (cód 1): {genero_percent.get(1, 0):.2f}% (Contagem: {genero_counts.get(1,0)})")
        print(f"Feminino (cód 2): {genero_percent.get(2, 0):.2f}% (Contagem: {genero_counts.get(2,0)})")
        # Incluir outros códigos se existirem e forem relevantes
        outros_cods = [cod for cod in genero_counts.index if cod not in [1, 2]]
        outros_p = sum(genero_percent.get(cod, 0) for cod in outros_cods)
        outros_c = sum(genero_counts.get(cod, 0) for cod in outros_cods)
        print(f"Outros/Prefiro não responder (códs {outros_cods}): {outros_p:.2f}% (Contagem: {outros_c})")
    else:
        print("\nAVISO: Coluna 'GENERO_COD' não encontrada.")

    # Nível de Jogador (usando NIVEL_JOGADOR_COD)
    # Mapeamento reverso: {1: 'Amador/Jogador casual', 2: 'Semi-Profissional', 3: 'Profissional'}
    if 'NIVEL_JOGADOR_COD' in df.columns:
        print("\n--- NÍVEL DE JOGADOR (baseado em NIVEL_JOGADOR_COD) ---")
        nivel_counts = df['NIVEL_JOGADOR_COD'].value_counts()
        nivel_percent = df['NIVEL_JOGADOR_COD'].value_counts(normalize=True) * 100
        print(f"Amador/Casual (cód 1): {nivel_percent.get(1, 0):.2f}% (Contagem: {nivel_counts.get(1,0)})")
        print(f"Semi-Profissional (cód 2): {nivel_percent.get(2, 0):.2f}% (Contagem: {nivel_counts.get(2,0)})")
        print(f"Profissional (cód 3): {nivel_percent.get(3, 0):.2f}% (Contagem: {nivel_counts.get(3,0)})")
    else:
        print("\nAVISO: Coluna 'NIVEL_JOGADOR_COD' não encontrada.")

    # Consumo de Cafeína Total Diário (MG_CAFEINA_DIA)
    if 'MG_CAFEINA_DIA' in df.columns:
        print("\n--- CONSUMO DE CAFEÍNA (MG_CAFEINA_DIA) ---")
        print(f"Média de Cafeína por Dia: {df['MG_CAFEINA_DIA'].mean():.2f} mg")
        print(f"Desvio Padrão de Cafeína por Dia: {df['MG_CAFEINA_DIA'].std():.2f} mg")
        print(f"Mediana de Cafeína por Dia: {df['MG_CAFEINA_DIA'].median():.2f} mg")
        print(f"Mínimo de Cafeína por Dia: {df['MG_CAFEINA_DIA'].min()} mg")
        print(f"Máximo de Cafeína por Dia: {df['MG_CAFEINA_DIA'].max()} mg")
        nan_percent_cafeina = df['MG_CAFEINA_DIA'].isna().sum() / len(df) * 100
        print(f"Porcentagem de NaN em MG_CAFEINA_DIA: {nan_percent_cafeina:.2f}%")
    else:
        print("\nAVISO: Coluna 'MG_CAFEINA_DIA' não encontrada.")

    # Horas de Jogo Principal por Dia (HORAS_JOGO_PRINCIPAL_MEDIA_DIA)
    if 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' in df.columns:
        print("\n--- HORAS DE JOGO PRINCIPAL POR DIA (HORAS_JOGO_PRINCIPAL_MEDIA_DIA) ---")
        print(f"Média de Horas de Jogo: {df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'].mean():.2f} horas")
        print(f"Desvio Padrão de Horas de Jogo: {df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'].std():.2f} horas")
        print(f"Mediana de Horas de Jogo: {df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'].median():.2f} horas")
        print(f"Mínimo de Horas de Jogo: {df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'].min()} horas")
        print(f"Máximo de Horas de Jogo: {df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'].max()} horas")
    else:
        print("\nAVISO: Coluna 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' não encontrada.")

    # Consome Café (CONSUMO_CAFE_BIN)
    if 'CONSUMO_CAFE_BIN' in df.columns:
        print("\n--- CONSOME CAFÉ (CONSUMO_CAFE_BIN) ---")
        cafe_counts = df['CONSUMO_CAFE_BIN'].value_counts()
        cafe_percent = df['CONSUMO_CAFE_BIN'].value_counts(normalize=True) * 100
        print(f"Sim (cód 1): {cafe_percent.get(1, 0):.2f}% (Contagem: {cafe_counts.get(1,0)})")
        print(f"Não (cód 0): {cafe_percent.get(0, 0):.2f}% (Contagem: {cafe_counts.get(0,0)})")
    else:
        print("\nAVISO: Coluna 'CONSUMO_CAFE_BIN' não encontrada.")

    # Consome Energéticos (CONSUMO_ENERGETICOS_BIN)
    if 'CONSUMO_ENERGETICOS_BIN' in df.columns:
        print("\n--- CONSOME ENERGÉTICOS (CONSUMO_ENERGETICOS_BIN) ---")
        energeticos_counts = df['CONSUMO_ENERGETICOS_BIN'].value_counts()
        energeticos_percent = df['CONSUMO_ENERGETICOS_BIN'].value_counts(normalize=True) * 100
        print(f"Sim (cód 1): {energeticos_percent.get(1, 0):.2f}% (Contagem: {energeticos_counts.get(1,0)})")
        print(f"Não (cód 0): {energeticos_percent.get(0, 0):.2f}% (Contagem: {energeticos_counts.get(0,0)})")
    else:
        print("\nAVISO: Coluna 'CONSUMO_ENERGETICOS_BIN' não encontrada.")
        
    # Adicione aqui mais estatísticas conforme necessário para o AED_Resultados_Chave.md
    # Exemplo: Distribuição de NaN geral por coluna
    print("\n--- PORCENTAGEM DE DADOS AUSENTES (NaN) POR COLUNA (mostrar todas com NaN > 0) ---")
    nan_summary = df.isna().mean() * 100 # .mean() em booleano é a mesma coisa que .sum()/len()
    nan_summary = nan_summary[nan_summary > 0].sort_values(ascending=False)
    if not nan_summary.empty:
        for col, perc_nan in nan_summary.items():
            print(f"{col}: {perc_nan:.2f}%")
    else:
        print("Nenhuma coluna com dados ausentes encontrada.")

if __name__ == '__main__':
    # Caminho para o arquivo CSV processado
    caminho_do_arquivo_csv = 'C:/Users/nicol_qs45gn8/IC/IC_Dados_Processados.csv' # Usando caminho absoluto
    calcular_estatisticas_descritivas(caminho_do_arquivo_csv) 