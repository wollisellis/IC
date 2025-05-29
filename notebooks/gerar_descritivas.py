import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "notebooks/outputs"

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def format_table_markdown(header, data_rows):
    """Formats data into a Markdown table string."""
    table_str = "| " + " | ".join(header) + " |\\n"
    table_str += "|-" + "-|-".join(["-" * len(h) for h in header]) + "-|\\n"
    for row in data_rows:
        table_str += "| " + " | ".join(map(str, row)) + " |\\n"
    return table_str

def calcular_estatisticas_descritivas(caminho_csv: str):
    """
    Calcula e imprime estatísticas descritivas de colunas chave
    do arquivo IC_Dados_Processados.csv em formato Markdown.
    """
    try:
        df = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        print(f"ERRO: O arquivo {caminho_csv} não foi encontrado.")
        print("Certifique-se de que o script run_pipeline.py foi executado e gerou o arquivo.")
        return

    print("\n## Tabela 1: Características Sociodemográficas e de Jogo da Amostra (N=181)\\n")
    
    table1_header = ["Característica", "Estatística", "Valor"]
    table1_data = []

    # Número total de participantes
    table1_data.append(["Participantes", "Total (N)", len(df)])

    # Idade
    if 'IDADE' in df.columns:
        table1_data.append(["Idade", "Média (DP)", f"{df['IDADE'].mean():.2f} (DP = {df['IDADE'].std():.2f})"])
        table1_data.append(["Idade", "Mínimo - Máximo", f"{df['IDADE'].min():.0f} - {df['IDADE'].max():.0f}"])
    else:
        table1_data.append(["Idade", "Status", "Coluna 'IDADE' não encontrada"])

    # Gênero
    if 'GENERO_COD' in df.columns:
        genero_counts = df['GENERO_COD'].value_counts()
        genero_percent = df['GENERO_COD'].value_counts(normalize=True) * 100
        table1_data.append(["Gênero", "Masculino (N, %)", f"{genero_counts.get(1,0)} ({genero_percent.get(1, 0):.2f}%)"])
        table1_data.append(["Gênero", "Feminino (N, %)", f"{genero_counts.get(2,0)} ({genero_percent.get(2, 0):.2f}%)"])
        outros_cods = [cod for cod in genero_counts.index if cod not in [1, 2]]
        outros_c = sum(genero_counts.get(cod, 0) for cod in outros_cods)
        outros_p = sum(genero_percent.get(cod, 0) for cod in outros_cods)
        table1_data.append(["Gênero", f"Outros/PÑR (códs {outros_cods}) (N, %)", f"{outros_c} ({outros_p:.2f}%)"])
    else:
        table1_data.append(["Gênero", "Status", "Coluna 'GENERO_COD' não encontrada"])

    # Nível de Jogador
    if 'NIVEL_JOGADOR_COD' in df.columns:
        nivel_counts = df['NIVEL_JOGADOR_COD'].value_counts()
        nivel_percent = df['NIVEL_JOGADOR_COD'].value_counts(normalize=True) * 100
        table1_data.append(["Nível de Jogador", "Amador/Casual (N, %)", f"{nivel_counts.get(1,0)} ({nivel_percent.get(1, 0):.2f}%)"])
        table1_data.append(["Nível de Jogador", "Semi-Profissional (N, %)", f"{nivel_counts.get(2,0)} ({nivel_percent.get(2, 0):.2f}%)"])
        table1_data.append(["Nível de Jogador", "Profissional (N, %)", f"{nivel_counts.get(3,0)} ({nivel_percent.get(3, 0):.2f}%)"])
    else:
        table1_data.append(["Nível de Jogador", "Status", "Coluna 'NIVEL_JOGADOR_COD' não encontrada"])

    # Horas de Jogo Principal por Dia
    if 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' in df.columns:
        table1_data.append(["Horas de Jogo Principal/Dia", "Média (DP)", f"{df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'].mean():.2f} (DP = {df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'].std():.2f})"])
        table1_data.append(["Horas de Jogo Principal/Dia", "Mediana", f"{df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'].median():.2f}"])
    else:
        table1_data.append(["Horas de Jogo Principal/Dia", "Status", "Coluna 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' não encontrada"])
    
    print(format_table_markdown(table1_header, table1_data))

    # --- Tabela 2: Parte A --- 
    print("\n## Tabela 2: Padrões de Consumo de Cafeína e Resultados dos Testes de Hipóteses\\n")
    print("### Parte A: Consumo de Cafeína Total Diário (MG_CAFEINA_DIA)\\n")

    table2a_header = ["Descrição", "Estatística", "Valor (mg)"]
    table2a_data = []

    if 'MG_CAFEINA_DIA' in df.columns and 'NIVEL_JOGADOR_COD' in df.columns:
        table2a_data.append(["Geral", "Média (DP)", f"{df['MG_CAFEINA_DIA'].mean():.2f} (DP = {df['MG_CAFEINA_DIA'].std():.2f})"])
        table2a_data.append(["Geral", "Mediana", f"{df['MG_CAFEINA_DIA'].median():.2f}"])
        table2a_data.append(["Geral", "Mínimo - Máximo", f"{df['MG_CAFEINA_DIA'].min():.2f} - {df['MG_CAFEINA_DIA'].max():.2f}"])
        
        # Por Nível de Jogador (Amador/Casual e Semi-Profissional)
        cafeina_amador = df[df['NIVEL_JOGADOR_COD'] == 1]['MG_CAFEINA_DIA']
        cafeina_semi = df[df['NIVEL_JOGADOR_COD'] == 2]['MG_CAFEINA_DIA']

        if not cafeina_amador.empty:
            table2a_data.append(["Amador/Casual", "Média (DP)", f"{cafeina_amador.mean():.2f} (DP = {cafeina_amador.std():.2f})"])
            table2a_data.append(["Amador/Casual", "Mediana", f"{cafeina_amador.median():.2f}"])
        else:
            table2a_data.append(["Amador/Casual", "Status", "Dados não disponíveis ou Nível não encontrado"])

        if not cafeina_semi.empty:
            table2a_data.append(["Semi-Profissional", "Média (DP)", f"{cafeina_semi.mean():.2f} (DP = {cafeina_semi.std():.2f})"])
            table2a_data.append(["Semi-Profissional", "Mediana", f"{cafeina_semi.median():.2f}"])
        else:
            table2a_data.append(["Semi-Profissional", "Status", "Dados não disponíveis ou Nível não encontrado"])
        
        nan_percent_cafeina = df['MG_CAFEINA_DIA'].isna().sum() / len(df) * 100
        table2a_data.append(["Geral", "% NaN", f"{nan_percent_cafeina:.2f}%"])
    else:
        table2a_data.append(["Consumo de Cafeína", "Status", "Colunas 'MG_CAFEINA_DIA' ou 'NIVEL_JOGADOR_COD' não encontradas"])

    print(format_table_markdown(table2a_header, table2a_data))

    # --- Geração de Figuras ---
    ensure_output_dir()

    # Figura 1: Distribuição do Consumo Diário de Cafeína (MG_CAFEINA_DIA)
    if 'MG_CAFEINA_DIA' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.hist(df['MG_CAFEINA_DIA'].dropna(), bins=20, color='skyblue', edgecolor='black')
        plt.title('Figura 1: Distribuição do Consumo Diário de Cafeína (MG_CAFEINA_DIA)')
        plt.xlabel('Consumo Diário de Cafeína (mg)')
        plt.ylabel('Frequência')
        plt.grid(axis='y', alpha=0.75)
        fig1_path = os.path.join(OUTPUT_DIR, "figura1_distribuicao_cafeina.png")
        plt.savefig(fig1_path)
        plt.close()
        print(f"\\nFigura 1 salva em: {fig1_path}")
    else:
        print("\\nAVISO: Não foi possível gerar a Figura 1 (Coluna 'MG_CAFEINA_DIA' não encontrada).")

    # Figura 2: Consumo Diário de Cafeína (MG_CAFEINA_DIA) por Nível de Jogador
    if 'MG_CAFEINA_DIA' in df.columns and 'NIVEL_JOGADOR_COD' in df.columns:
        # Mapear códigos para nomes para melhor visualização
        df_copy = df.copy()
        nivel_map = {1: 'Amador/Casual', 2: 'Semi-Profissional', 3: 'Profissional'}
        df_copy['NIVEL_JOGADOR_NOME'] = df_copy['NIVEL_JOGADOR_COD'].map(nivel_map)
        
        # Considerar apenas Amador/Casual e Semi-Profissional devido ao N baixo de Profissional
        df_plot_fig2 = df_copy[df_copy['NIVEL_JOGADOR_COD'].isin([1, 2])]
        
        if not df_plot_fig2.empty:
            plt.figure(figsize=(10, 6))
            df_plot_fig2.boxplot(column='MG_CAFEINA_DIA', by='NIVEL_JOGADOR_NOME', grid=True, patch_artist=True)
            plt.title('Figura 2: Consumo Diário de Cafeína por Nível de Jogador')
            plt.suptitle('') # Remove o título automático do pandas
            plt.xlabel('Nível do Jogador')
            plt.ylabel('Consumo Diário de Cafeína (mg)')
            fig2_path = os.path.join(OUTPUT_DIR, "figura2_cafeina_por_nivel.png")
            plt.savefig(fig2_path)
            plt.close()
            print(f"Figura 2 salva em: {fig2_path}")
        else:
            print("\\nAVISO: Não foi possível gerar a Figura 2 (Dados insuficientes para os níveis de jogador especificados).")
    else:
        print("\\nAVISO: Não foi possível gerar a Figura 2 (Colunas 'MG_CAFEINA_DIA' ou 'NIVEL_JOGADOR_COD' não encontradas).")

    # Outras estatísticas descritivas (mantidas para informação, mas não parte das tabelas principais da tese)
    print("\n--- Outras Estatísticas Descritivas (para informação) ---")
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