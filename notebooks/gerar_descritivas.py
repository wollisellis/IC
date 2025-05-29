import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

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

    # Figura 1: Distribuição do Consumo Diário Total de Cafeína (mg)
    if 'MG_CAFEINA_DIA' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.hist(df['MG_CAFEINA_DIA'].dropna(), bins=20, color='skyblue', edgecolor='black')
        plt.title('Figura 1: Distribuição do Consumo Diário Total de Cafeína')
        plt.xlabel('Consumo Diário Total de Cafeína (mg)')
        plt.ylabel('Frequência (Número de Participantes)')
        plt.grid(axis='y', alpha=0.75)
        fig1_path = os.path.join(OUTPUT_DIR, "figura1_distribuicao_cafeina.png")
        plt.savefig(fig1_path)
        plt.close()
        print(f"\nFigura 1 salva em: {fig1_path}")
    else:
        print("\nAVISO: Não foi possível gerar a Figura 1 (Coluna 'MG_CAFEINA_DIA' não encontrada).")

    # Figura 2: Consumo Diário Total de Cafeína por Nível de Experiência do Jogador
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
            plt.title('Figura 2: Consumo Diário Total de Cafeína por Nível de Experiência do Jogador')
            plt.xlabel('Nível de Experiência do Jogador')
            plt.ylabel('Consumo Diário Total de Cafeína (mg)')
            plt.suptitle('') # Remove o título automático do pandas
            fig2_path = os.path.join(OUTPUT_DIR, "figura2_cafeina_por_nivel.png")
            plt.savefig(fig2_path)
            plt.close()
            print(f"Figura 2 salva em: {fig2_path}")
        else:
            print("\nAVISO: Não foi possível gerar a Figura 2 (Dados insuficientes para os níveis de jogador especificados).")
    else:
        print("\nAVISO: Não foi possível gerar a Figura 2 (Colunas 'MG_CAFEINA_DIA' ou 'NIVEL_JOGADOR_COD' não encontradas).")

    # Figura 3: Consumo Diário de Cafeína (MG_CAFEINA_DIA) por Intenção de Melhorar Performance
    if 'MG_CAFEINA_DIA' in df.columns and 'MELHORAR_PERFORMANCE_MOTIVO_BIN' in df.columns:
        df_copy_h7 = df.copy()
        performance_map = {0: 'Não visa Performance', 1: 'Visa Performance'}
        df_copy_h7['PERFORMANCE_MOTIVO_NOME'] = df_copy_h7['MELHORAR_PERFORMANCE_MOTIVO_BIN'].map(performance_map)
        
        df_plot_fig3 = df_copy_h7.dropna(subset=['MG_CAFEINA_DIA', 'PERFORMANCE_MOTIVO_NOME'])

        if not df_plot_fig3.empty and df_plot_fig3['PERFORMANCE_MOTIVO_NOME'].nunique() >= 2:
            plt.figure(figsize=(10, 6))
            order = ['Não visa Performance', 'Visa Performance'] # Garantir a ordem correta no plot
            sns.boxplot(x='PERFORMANCE_MOTIVO_NOME', y='MG_CAFEINA_DIA', data=df_plot_fig3, order=order, palette="pastel")
            plt.title('Figura 3: Consumo Diário de Cafeína por Intenção de Melhorar Performance')
            plt.xlabel('Consome Cafeína para Melhorar Performance?')
            plt.ylabel('Consumo Diário de Cafeína (mg)')
            plt.grid(axis='y', alpha=0.75)
            fig3_path = os.path.join(OUTPUT_DIR, "figura3_cafeina_por_performance.png")
            plt.savefig(fig3_path)
            plt.close()
            print(f"Figura 3 salva em: {fig3_path}")
        else:
            print("\nAVISO: Não foi possível gerar a Figura 3 (Dados insuficientes ou um único grupo após filtro para 'MELHORAR_PERFORMANCE_MOTIVO_BIN').")
    else:
        print("\nAVISO: Não foi possível gerar a Figura 3 (Colunas 'MG_CAFEINA_DIA' ou 'MELHORAR_PERFORMANCE_MOTIVO_BIN' não encontradas).")

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

    # Adicionar contagens para variáveis específicas de interesse para novas hipóteses
    print("\n--- Contagens para Variáveis de Interesse Adicionais ---")

    if 'PLATAFORMA_PRINCIPAL_COD' in df.columns:
        print("\n--- PLATAFORMA PRINCIPAL (PLATAFORMA_PRINCIPAL_COD) ---")
        # Códigos conforme Livro_de_Codigos.txt (e data_processing.py)
        map_plataforma = {
            1: 'PC',
            2: 'Celular/Mobile',
            3: 'Playstation',
            4: 'Xbox',
            5: 'Nintendo',
            6: 'Outro'
        }
        plataforma_counts = df['PLATAFORMA_PRINCIPAL_COD'].value_counts()
        plataforma_percent = df['PLATAFORMA_PRINCIPAL_COD'].value_counts(normalize=True) * 100
        for cod, count in plataforma_counts.items():
            label = map_plataforma.get(cod, f'Código {cod} não mapeado')
            print(f"{label}: {plataforma_percent.get(cod, 0):.2f}% (Contagem: {count})")
        if df['PLATAFORMA_PRINCIPAL_COD'].isna().any():
             print(f"NaNs: {df['PLATAFORMA_PRINCIPAL_COD'].isna().sum() / len(df) * 100:.2f}% (Contagem: {df['PLATAFORMA_PRINCIPAL_COD'].isna().sum()})")
    else:
        print("\nAVISO: Coluna 'PLATAFORMA_PRINCIPAL_COD' não encontrada.")

    if 'EFEITO_ADVERSO_PRESENTE_BIN' in df.columns:
        print("\n--- EFEITO ADVERSO PRESENTE (EFEITO_ADVERSO_PRESENTE_BIN) ---")
        ea_counts = df['EFEITO_ADVERSO_PRESENTE_BIN'].value_counts()
        ea_percent = df['EFEITO_ADVERSO_PRESENTE_BIN'].value_counts(normalize=True) * 100
        print(f"Sim (cód 1): {ea_percent.get(1, 0):.2f}% (Contagem: {ea_counts.get(1,0)})")
        print(f"Não (cód 0): {ea_percent.get(0, 0):.2f}% (Contagem: {ea_counts.get(0,0)})")
        if df['EFEITO_ADVERSO_PRESENTE_BIN'].isna().any():
             print(f"NaNs: {df['EFEITO_ADVERSO_PRESENTE_BIN'].isna().sum() / len(df) * 100:.2f}% (Contagem: {df['EFEITO_ADVERSO_PRESENTE_BIN'].isna().sum()})")
    else:
        print("\nAVISO: Coluna 'EFEITO_ADVERSO_PRESENTE_BIN' não encontrada.")

    if 'MELHORAR_PERFORMANCE_MOTIVO_BIN' in df.columns:
        print("\n--- MOTIVO MELHORAR PERFORMANCE (MELHORAR_PERFORMANCE_MOTIVO_BIN) ---")
        perf_counts = df['MELHORAR_PERFORMANCE_MOTIVO_BIN'].value_counts(dropna=False) # Incluir NaNs na contagem inicial
        perf_percent = df['MELHORAR_PERFORMANCE_MOTIVO_BIN'].value_counts(normalize=True, dropna=False) * 100
        
        # Contagem para Sim (1.0)
        sim_count = perf_counts.get(1.0, 0)
        sim_percent = (sim_count / len(df)) * 100 if len(df) > 0 else 0
        print(f"Sim (cód 1): {sim_percent:.2f}% (Contagem: {sim_count})")
        
        # Contagem para Não (0.0)
        nao_count = perf_counts.get(0.0, 0)
        nao_percent = (nao_count / len(df)) * 100 if len(df) > 0 else 0
        print(f"Não (cód 0): {nao_percent:.2f}% (Contagem: {nao_count})")

        # Contagem para NaNs
        nan_count = df['MELHORAR_PERFORMANCE_MOTIVO_BIN'].isna().sum()
        nan_percent = (nan_count / len(df)) * 100 if len(df) > 0 else 0
        if nan_count > 0:
            print(f"NaNs: {nan_percent:.2f}% (Contagem: {nan_count})")
    else:
        print("\nAVISO: Coluna 'MELHORAR_PERFORMANCE_MOTIVO_BIN' não encontrada.")

    print("\n\\n--- Contagens Detalhadas e Figuras para Efeitos Adversos Específicos (H3) ---")
    efeitos_para_analise_descritiva = {
        'EFEITO_ADVERSO_INSONIA_BIN': 'Insônia',
        'EFEITO_ADVERSO_TAQUICARDIA_BIN': 'Taquicardia',
        'EFEITO_ADVERSO_TREMORES_BIN': 'Tremores',
        'EFEITO_ADVERSO_DOR_ESTOMAGO_BIN': 'Dor no Estômago'
    }

    for col_bin, nome_efeito_fig in efeitos_para_analise_descritiva.items():
        print(f"\\n--- EFEITO ADVERSO: {nome_efeito_fig} ({col_bin}) ---")
        if col_bin in df.columns:
            # Contagens
            counts = df[col_bin].value_counts(dropna=False)
            total_participantes = len(df)
            
            sim_count = counts.get(1, 0)
            sim_percent = (sim_count / total_participantes) * 100 if total_participantes > 0 else 0
            print(f"Com {nome_efeito_fig} (cód 1): {sim_percent:.2f}% (Contagem: {sim_count})")

            nao_count = counts.get(0, 0)
            nao_percent = (nao_count / total_participantes) * 100 if total_participantes > 0 else 0
            print(f"Sem {nome_efeito_fig} (cód 0): {nao_percent:.2f}% (Contagem: {nao_count})")
            
            nan_count = counts.get(np.nan, counts[counts.index.isna()].sum()) # Contar NaNs explicitamente
            nan_percent = (nan_count / total_participantes) * 100 if total_participantes > 0 else 0
            if nan_count > 0:
                print(f"NaNs: {nan_percent:.2f}% (Contagem: {nan_count})")

            # Figura (Boxplot: MG_CAFEINA_TOTAL_DIA vs. Presença do Efeito)
            if 'MG_CAFEINA_TOTAL_DIA' in df.columns:
                df_fig_h3 = df.copy()
                # Mapear 0 e 1 para rótulos mais descritivos para o plot
                map_efeito = {0: f'Sem {nome_efeito_fig}', 1: f'Com {nome_efeito_fig}'}
                df_fig_h3[f'{col_bin}_NOME'] = df_fig_h3[col_bin].map(map_efeito)
                
                df_plot_fig_h3_especifico = df_fig_h3.dropna(subset=['MG_CAFEINA_TOTAL_DIA', f'{col_bin}_NOME'])

                if not df_plot_fig_h3_especifico.empty and df_plot_fig_h3_especifico[f'{col_bin}_NOME'].nunique() >= 2:
                    plt.figure(figsize=(10, 6))
                    order_h3 = [f'Sem {nome_efeito_fig}', f'Com {nome_efeito_fig}']
                    sns.boxplot(x=f'{col_bin}_NOME', y='MG_CAFEINA_TOTAL_DIA', data=df_plot_fig_h3_especifico, order=order_h3, palette="pastel")
                    plt.title(f'Figura H3 ({nome_efeito_fig}): Consumo de Cafeína vs. {nome_efeito_fig}')
                    plt.xlabel(f'Reportou {nome_efeito_fig}?')
                    plt.ylabel('Consumo Diário de Cafeína (mg)')
                    plt.grid(axis='y', alpha=0.75)
                    fig_h3_path = os.path.join(OUTPUT_DIR, f"figura_H3_{nome_efeito_fig.lower().replace(' ', '_').replace('ô', 'o')}.png")
                    plt.savefig(fig_h3_path)
                    plt.close()
                    print(f"Figura H3 ({nome_efeito_fig}) salva em: {fig_h3_path}")
                else:
                    print(f"AVISO: Não foi possível gerar a Figura H3 para {nome_efeito_fig} (Dados insuficientes ou um único grupo após filtro).")
            else:
                print(f"AVISO: Não foi possível gerar a Figura H3 para {nome_efeito_fig} (Coluna 'MG_CAFEINA_TOTAL_DIA' não encontrada).")
        else:
            print(f"AVISO: Coluna '{col_bin}' não encontrada para {nome_efeito_fig}.")

if __name__ == '__main__':
    # Caminho para o arquivo CSV processado
    caminho_do_arquivo_csv = 'C:/Users/nicol_qs45gn8/IC/IC_Dados_Processados.csv' # Usando caminho absoluto
    calcular_estatisticas_descritivas(caminho_do_arquivo_csv) 