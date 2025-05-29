print("--- INÍCIO DA EXECUÇÃO DO SCRIPT DE ANÁLISES INFERENCIAIS ---")
"""
Script para realizar análises estatísticas inferenciais para o estudo
de consumo de cafeína em jogadores de e-sports.
"""
import pandas as pd
from scipy.stats import kruskal, pearsonr, spearmanr, mannwhitneyu, chi2_contingency, fisher_exact
import statsmodels.api as sm
from statsmodels.formula.api import ols
import scikit_posthocs as sp
import numpy as np

def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    """Carrega os dados processados."""
    try:
        df = pd.read_csv(caminho_csv)
        print(f"Dados carregados com sucesso de {caminho_csv}")
        print(f"Shape do DataFrame: {df.shape}")
        colunas_numericas_chave = ['MG_CAFEINA_TOTAL_DIA', 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA']
        for col in colunas_numericas_chave:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                print(f"AVISO: Coluna numérica chave {col} não encontrada.")

        colunas_categoricas_chave = ['NIVEL_JOGADOR_COD', 'EFEITO_ADVERSO_INSONIA_BIN', 'EFEITO_ADVERSO_NERVOSISMO_BIN']
        for col in colunas_categoricas_chave:
            if col not in df.columns:
                print(f"AVISO: Coluna categórica chave {col} não encontrada.")
        return df
    except FileNotFoundError:
        print(f"ERRO: O arquivo {caminho_csv} não foi encontrado.")
        return pd.DataFrame()

def analisar_h1(df: pd.DataFrame):
    """
    H1: Jogadores profissionais consomem mais cafeína diariamente que amadores.
    Testa diferenças no consumo de cafeína (MG_CAFEINA_TOTAL_DIA)
    entre diferentes níveis de jogadores (NIVEL_JOGADOR_COD).
    """
    print("\n--- Análise H1: Consumo de Cafeína vs. Nível do Jogador ---")
    if 'MG_CAFEINA_TOTAL_DIA' not in df.columns or 'NIVEL_JOGADOR_COD' not in df.columns:
        print("Colunas necessárias para H1 (MG_CAFEINA_TOTAL_DIA, NIVEL_JOGADOR_COD) não encontradas. Pulando análise.")
        return

    df_h1 = df[['NIVEL_JOGADOR_COD', 'MG_CAFEINA_TOTAL_DIA']].copy()
    df_h1.dropna(subset=['MG_CAFEINA_TOTAL_DIA', 'NIVEL_JOGADOR_COD'], inplace=True)

    if df_h1.empty:
        print("Não há dados suficientes para H1 após remover NaNs.")
        return

    niveis_no_csv = df_h1['NIVEL_JOGADOR_COD'].unique()
    print(f"Níveis de jogador encontrados no CSV para H1: {niveis_no_csv}")

    # Mapear códigos numéricos de NIVEL_JOGADOR_COD para rótulos
    map_nivel_jogador_esperado = {
        1: 'Amador/Casual',
        2: 'Semi-Profissional',
        3: 'Profissional'
    }

    grupos_para_teste = []
    nomes_dos_grupos_map = {}
    
    df_h1_filtrado = df_h1.copy()

    for codigo, nome in map_nivel_jogador_esperado.items():
        if codigo in niveis_no_csv:
            dados_do_grupo = df_h1[df_h1['NIVEL_JOGADOR_COD'] == codigo]['MG_CAFEINA_TOTAL_DIA']
            if not dados_do_grupo.empty:
                grupos_para_teste.append(dados_do_grupo)
                nomes_dos_grupos_map[nome] = dados_do_grupo
                print(f"Grupo '{nome}': N={len(dados_do_grupo)}, Média Cafeína={dados_do_grupo.mean():.2f} mg, DP={dados_do_grupo.std():.2f} mg")
            else:
                print(f"Grupo '{nome}' encontrado mas vazio após filtro de NaN para cafeína.")
        else:
            print(f"Nível esperado '{nome}' não encontrado diretamente nos dados de NIVEL_JOGADOR_COD.")

    if len(grupos_para_teste) < 2:
        print("Não foi possível formar pelo menos dois grupos para o teste H1. Verifique os valores em NIVEL_JOGADOR_COD.")
        return

    p_valor_h1 = 1.0
    try:
        if len(grupos_para_teste) == 2:
            stat, p_valor_h1 = mannwhitneyu(grupos_para_teste[0], grupos_para_teste[1], alternative='two-sided')
            print(f"Teste Mann-Whitney U entre '{list(nomes_dos_grupos_map.keys())[0]}' e '{list(nomes_dos_grupos_map.keys())[1]}': Estatística U={stat:.2f}, p-valor={p_valor_h1:.4f}")
        elif len(grupos_para_teste) >= 3:
            stat, p_valor_h1 = kruskal(*grupos_para_teste)
            print(f"Teste Kruskal-Wallis entre os {len(nomes_dos_grupos_map.keys())} grupos ({', '.join(nomes_dos_grupos_map.keys())}): H-estatística={stat:.2f}, p-valor={p_valor_h1:.4f}")
        
        if p_valor_h1 < 0.05:
            print("Resultado H1: Diferença estatisticamente significativa encontrada.")
            if len(grupos_para_teste) >= 3:
                print("\n  Realizando teste post-hoc de Dunn com correção de Bonferroni:")
                posthoc_df = sp.posthoc_dunn(grupos_para_teste, p_adjust='bonferroni')
                
                group_names_list = list(nomes_dos_grupos_map.keys())
                posthoc_df.columns = group_names_list
                posthoc_df.index = group_names_list
                print("  Matriz de p-valores (Teste de Dunn com correção de Bonferroni):")
                print(posthoc_df)
                
                print("\n  Interpretação do Post-Hoc (Dunn-Bonferroni):")
                for i in range(len(group_names_list)):
                    for j in range(i + 1, len(group_names_list)):
                        group1 = group_names_list[i]
                        group2 = group_names_list[j]
                        p_value = posthoc_df.loc[group1, group2]
                        if p_value < 0.05:
                            print(f"    Diferença significativa encontrada entre '{group1}' e '{group2}' (p={p_value:.4f})")
                        else:
                            print(f"    NÃO houve diferença significativa entre '{group1}' e '{group2}' (p={p_value:.4f})")
        else:
            print("Resultado H1: Nenhuma diferença estatisticamente significativa encontrada.")
    except Exception as e:
        print(f"Erro ao executar o teste para H1: {e}")

def analisar_h2(df: pd.DataFrame):
    """
    H2: Maior consumo de cafeína está associado a maior tempo médio de jogo por dia.
    Testa correlação entre MG_CAFEINA_TOTAL_DIA e HORAS_JOGO_PRINCIPAL_MEDIA_DIA.
    """
    print("\n--- Análise H2: Consumo de Cafeína vs. Horas de Jogo ---")
    if 'MG_CAFEINA_TOTAL_DIA' not in df.columns or 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' not in df.columns:
        print("Colunas necessárias para H2 (MG_CAFEINA_TOTAL_DIA, HORAS_JOGO_PRINCIPAL_MEDIA_DIA) não encontradas. Pulando.")
        return

    df_h2 = df[['MG_CAFEINA_TOTAL_DIA', 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA']].copy()
    df_h2.dropna(inplace=True)

    if df_h2.empty or len(df_h2) < 5:
        print(f"Não há dados suficientes para H2 após remover NaNs (mínimo 5, encontrados: {len(df_h2)}). Pulando.")
        return

    cafeina = df_h2['MG_CAFEINA_TOTAL_DIA']
    horas_jogo = df_h2['HORAS_JOGO_PRINCIPAL_MEDIA_DIA']

    try:
        corr_pearson, p_pearson = pearsonr(cafeina, horas_jogo)
        print(f"Correlação de Pearson: r={corr_pearson:.3f}, p-valor={p_pearson:.4f}")
        if p_pearson < 0.05:
            print("Resultado (Pearson) H2: Correlação estatisticamente significativa.")
        else:
            print("Resultado (Pearson) H2: Nenhuma correlação estatisticamente significativa.")
    except Exception as e:
        print(f"Erro ao calcular Correlação de Pearson para H2: {e}")

    try:
        corr_spearman, p_spearman = spearmanr(cafeina, horas_jogo)
        print(f"Correlação de Spearman: rho={corr_spearman:.3f}, p-valor={p_spearman:.4f}")
        if p_spearman < 0.05:
            print("Resultado (Spearman) H2: Correlação estatisticamente significativa.")
        else:
            print("Resultado (Spearman) H2: Nenhuma correlação estatisticamente significativa.")
    except Exception as e:
        print(f"Erro ao calcular Correlação de Spearman para H2: {e}")

def analisar_h3(df: pd.DataFrame):
    """
    H3: Frequência de efeitos adversos (insônia, nervosismo) aumenta conforme a dose de cafeína.
    Compara MG_CAFEINA_TOTAL_DIA entre quem reporta (BIN=1) e não reporta (BIN=0) os efeitos.
    """
    print("\n--- Análise H3: Efeitos Adversos vs. Dose de Cafeína ---")
    efeitos_colunas_binarias = {
        'EFEITO_ADVERSO_INSONIA_BIN': 'Insônia',
        'EFEITO_ADVERSO_TAQUICARDIA_BIN': 'Taquicardia',
        'EFEITO_ADVERSO_NERVOSISMO_BIN': 'Nervosismo',
        'EFEITO_ADVERSO_TREMORES_BIN': 'Tremores',
        'EFEITO_ADVERSO_DOR_ESTOMAGO_BIN': 'Dor no Estômago'
    }
    if 'MG_CAFEINA_TOTAL_DIA' not in df.columns:
        print("Coluna MG_CAFEINA_TOTAL_DIA não encontrada. Pulando H3.")
        return

    for col_bin, nome_efeito in efeitos_colunas_binarias.items():
        print(f"  Analisando efeito: {nome_efeito} (coluna: {col_bin})")
        if col_bin not in df.columns:
            print(f"    Coluna {col_bin} não encontrada. Pulando este efeito.")
            continue

        df_h3 = df[[col_bin, 'MG_CAFEINA_TOTAL_DIA']].copy()
        df_h3.dropna(inplace=True)
        
        if df_h3.empty:
            print(f"    Não há dados suficientes para {col_bin} após remover NaNs.")
            continue
        
        try:
            df_h3[col_bin] = pd.to_numeric(df_h3[col_bin], errors='raise').astype(int)
        except (ValueError, TypeError) as e:
            print(f"    Erro ao converter coluna {col_bin} para numérico/inteiro: {e}. Valores: {df_h3[col_bin].unique()[:5]}. Pulando.")
            continue

        valores_unicos_efeito = df_h3[col_bin].unique()
        if not all(v in [0, 1] for v in valores_unicos_efeito):
            print(f"    Coluna {col_bin} não é binária (0 ou 1) após conversão (valores: {valores_unicos_efeito}). Pulando.")
            continue

        grupo_com_efeito = df_h3[df_h3[col_bin] == 1]['MG_CAFEINA_TOTAL_DIA']
        grupo_sem_efeito = df_h3[df_h3[col_bin] == 0]['MG_CAFEINA_TOTAL_DIA']

        if grupo_com_efeito.empty or grupo_sem_efeito.empty or len(grupo_com_efeito) < 3 or len(grupo_sem_efeito) < 3:
            print(f"    Não há dados suficientes nos grupos COM e SEM {nome_efeito} para análise (min 3 por grupo). COM: {len(grupo_com_efeito)}, SEM: {len(grupo_sem_efeito)}.")
            continue

        try:
            # Teste unilateral: consumo de cafeína é MAIOR no grupo COM efeito
            stat, p_valor = mannwhitneyu(grupo_com_efeito, grupo_sem_efeito, alternative='greater')
            print(f"    Grupo COM {nome_efeito} (N={len(grupo_com_efeito)}): Média Cafeína={grupo_com_efeito.mean():.2f} mg (DP={grupo_com_efeito.std():.2f}) mg")
            print(f"    Grupo SEM {nome_efeito} (N={len(grupo_sem_efeito)}): Média Cafeína={grupo_sem_efeito.mean():.2f} mg (DP={grupo_sem_efeito.std():.2f}) mg")
            print(f"    Teste Mann-Whitney U (unilateral: COM {nome_efeito} > SEM {nome_efeito}): Estatística U={stat:.2f}, p-valor={p_valor:.4f}")
            if p_valor < 0.05:
                print(f"    Resultado H3 ({nome_efeito}): Consumo de cafeína é significativamente MAIOR no grupo COM {nome_efeito}.")
            else:
                print(f"    Resultado H3 ({nome_efeito}): Não há evidência de que o consumo de cafeína seja significativamente maior no grupo COM {nome_efeito}.")
        except Exception as e:
            print(f"    Erro ao realizar teste para {nome_efeito}: {e}")

def analisar_h7(df: pd.DataFrame):
    """
    H7: Jogadores que consomem cafeína para melhorar a performance 
    consomem mais cafeína do que os que não têm essa intenção.
    Testa diferenças no consumo de MG_CAFEINA_TOTAL_DIA entre
    MELHORAR_PERFORMANCE_MOTIVO_BIN (1 vs 0).
    """
    print("\n--- Análise H7: Consumo de Cafeína vs. Intenção de Melhorar Performance ---")
    col_interesse_h7 = 'MELHORAR_PERFORMANCE_MOTIVO_BIN'
    col_cafeina = 'MG_CAFEINA_TOTAL_DIA'

    if col_cafeina not in df.columns or col_interesse_h7 not in df.columns:
        print(f"Colunas necessárias para H7 ({col_cafeina}, {col_interesse_h7}) não encontradas. Pulando análise.")
        return

    df_h7 = df[[col_interesse_h7, col_cafeina]].copy()
    df_h7.dropna(subset=[col_interesse_h7, col_cafeina], inplace=True)

    if df_h7.empty:
        print("Não há dados suficientes para H7 após remover NaNs.")
        return
    
    try:
        df_h7[col_interesse_h7] = pd.to_numeric(df_h7[col_interesse_h7], errors='raise').astype(int)
    except (ValueError, TypeError) as e:
        print(f"    Erro ao converter coluna {col_interesse_h7} para numérico/inteiro: {e}. Valores: {df_h7[col_interesse_h7].unique()[:5]}. Pulando.")
        return

    valores_unicos_h7 = df_h7[col_interesse_h7].unique()
    if not all(v in [0, 1] for v in valores_unicos_h7):
        print(f"    Coluna {col_interesse_h7} não é binária (0 ou 1) após conversão (valores: {valores_unicos_h7}). Pulando.")
        return

    grupo_performance_sim = df_h7[df_h7[col_interesse_h7] == 1][col_cafeina]
    grupo_performance_nao = df_h7[df_h7[col_interesse_h7] == 0][col_cafeina]

    if grupo_performance_sim.empty or grupo_performance_nao.empty:
        print("    Não há dados suficientes em ambos os grupos (SIM e NÃO performance) para o teste.")
        if grupo_performance_sim.empty: print("      Ninguém reportou consumir para performance (ou todos com NaNs na cafeína associada).")
        if grupo_performance_nao.empty: print("      Todos reportaram consumir para performance (ou todos com NaNs na cafeína associada).")
        return
        
    print(f"    Grupo SIM Performance (N={len(grupo_performance_sim)}): Média Cafeína={grupo_performance_sim.mean():.2f} mg (DP={grupo_performance_sim.std():.2f}) mg")
    print(f"    Grupo NÃO Performance (N={len(grupo_performance_nao)}): Média Cafeína={grupo_performance_nao.mean():.2f} mg (DP={grupo_performance_nao.std():.2f}) mg")

    try:
        stat, p_valor = mannwhitneyu(grupo_performance_sim, grupo_performance_nao, alternative='greater') 
        print(f"    Teste Mann-Whitney U (unilateral: SIM Performance > NÃO Performance): Estatística U={stat:.2f}, p-valor={p_valor:.4f}")

        if p_valor < 0.05:
            print(f"    Resultado H7: Consumo de cafeína é significativamente MAIOR no grupo que visa performance.")
        else:
            print(f"    Resultado H7: Não há evidência de que o consumo de cafeína seja significativamente maior no grupo que visa performance.")
    except Exception as e:
        print(f"    Erro ao executar Mann-Whitney U para H7: {e}")

def analisar_h6(df: pd.DataFrame):
    """
    H6: Jogadores de diferentes plataformas principais (PC, console, mobile) 
    reportam diferentes perfis de efeitos adversos.
    Testa associação entre PLATAFORMA_PRINCIPAL_COD e EFEITO_ADVERSO_*_BIN.
    """
    print("\n--- Análise H6: Plataforma Principal vs. Efeitos Adversos ---")
    
    col_plataforma = 'PLATAFORMA_PRINCIPAL_COD'
    if col_plataforma not in df.columns:
        print(f"Coluna {col_plataforma} não encontrada. Pulando H6.")
        return

    # Efeitos adversos para analisar (aqueles com dados suficientes)
    efeitos_colunas_binarias_h6 = {
        'EFEITO_ADVERSO_INSONIA_BIN': 'Insônia',
        'EFEITO_ADVERSO_TAQUICARDIA_BIN': 'Taquicardia',
        'EFEITO_ADVERSO_TREMORES_BIN': 'Tremores',
        'EFEITO_ADVERSO_DOR_ESTOMAGO_BIN': 'Dor no Estômago'
    }
    
    # Mapeamento de códigos de plataforma para nomes (para logs mais claros)
    # Com base nas contagens: PC (1), Celular/Mobile (2), Playstation (3), Xbox (4)
    # Nintendo (5) e Outro (6) podem ter N muito baixo ou ser filtrados.
    map_plataforma_nomes = {
        1: 'PC',
        2: 'Celular/Mobile',
        3: 'Playstation',
        4: 'Xbox',
        5: 'Nintendo',
        6: 'Outro' 
    }

    for col_efeito, nome_efeito in efeitos_colunas_binarias_h6.items():
        print(f"\n  Analisando associação entre Plataforma e {nome_efeito} (coluna: {col_efeito})")
        if col_efeito not in df.columns:
            print(f"    Coluna de efeito {col_efeito} não encontrada. Pulando este efeito.")
            continue

        # Preparar dados para a tabela de contingência
        df_h6_efeito = df[[col_plataforma, col_efeito]].copy()
        df_h6_efeito.dropna(inplace=True) # Remove NaNs de ambas as colunas

        if df_h6_efeito.empty or len(df_h6_efeito) < 10: # Mínimo de 10 observações para uma análise razoável
            print(f"    Não há dados suficientes para {nome_efeito} e Plataforma após remover NaNs (N={len(df_h6_efeito)}). Pulando.")
            continue
        
        # Filtrar para plataformas com N > 0 após dropna
        # E opcionalmente com N mínimo (ex: N > 5) para estabilidade do teste qui-quadrado.
        # Por agora, vamos deixar o teste lidar com Ns baixos e usar Fisher se necessário.
        contagens_plataforma = df_h6_efeito[col_plataforma].value_counts()
        plataformas_com_dados = contagens_plataforma[contagens_plataforma > 0].index.tolist()
        
        # Mapear códigos para nomes para a tabela de contingência
        df_h6_efeito[col_plataforma] = df_h6_efeito[col_plataforma].map(map_plataforma_nomes)
        
        # Manter apenas plataformas que ainda existem após o dropna e têm nomes mapeados
        df_h6_efeito = df_h6_efeito[df_h6_efeito[col_plataforma].notna()]

        if df_h6_efeito[col_plataforma].nunique() < 2 or df_h6_efeito[col_efeito].nunique() < 2:
            print(f"    Menos de duas categorias em Plataforma ou {nome_efeito} após filtros. Pulando teste.")
            continue

        try:
            tabela_contingencia = pd.crosstab(df_h6_efeito[col_plataforma], df_h6_efeito[col_efeito])
            print("    Tabela de Contingência (Plataforma vs. Efeito Adverso):")
            print(tabela_contingencia)

            # Verificar se alguma contagem esperada é < 5
            chi2, p_valor, _, contagens_esperadas = chi2_contingency(tabela_contingencia)
            usar_fisher = False
            if np.any(contagens_esperadas < 5):
                print("    Alguma contagem esperada < 5. Usando Teste Exato de Fisher.")
                usar_fisher = True
            
            if usar_fisher:
                odds_ratio, p_valor_fisher = fisher_exact(tabela_contingencia)
                print(f"    Teste Exato de Fisher: Odds Ratio={odds_ratio:.2f}, p-valor={p_valor_fisher:.4f}")
                p_final = p_valor_fisher
            else:
                print(f"    Teste Qui-Quadrado: Chi2={chi2:.2f}, p-valor={p_valor:.4f}")
                p_final = p_valor

            if p_final < 0.05:
                print(f"    Resultado H6 ({nome_efeito}): Associação ESTATISTICAMENTE SIGNIFICATIVA encontrada entre Plataforma e {nome_efeito}.")
            else:
                print(f"    Resultado H6 ({nome_efeito}): NENHUMA associação estatisticamente significativa encontrada entre Plataforma e {nome_efeito}.")

        except Exception as e:
            print(f"    Erro ao executar teste de associação para {nome_efeito}: {e}")
            print(f"    Dados para {col_plataforma}: {df_h6_efeito[col_plataforma].unique()}")
            print(f"    Dados para {col_efeito}: {df_h6_efeito[col_efeito].unique()}")

def analisar_h8(df: pd.DataFrame):
    """
    H8: Existem diferenças no consumo diário de cafeína (MG_CAFEINA_TOTAL_DIA)
    entre participantes do gênero masculino (GENERO_COD=1) e feminino (GENERO_COD=2).
    """
    print("\n--- Análise H8: Consumo de Cafeína vs. Gênero ---")
    col_cafeina = 'MG_CAFEINA_TOTAL_DIA'
    col_genero = 'GENERO_COD'

    if col_cafeina not in df.columns or col_genero not in df.columns:
        print(f"Colunas necessárias para H8 ({col_cafeina}, {col_genero}) não encontradas. Pulando análise.")
        return

    df_h8 = df[[col_genero, col_cafeina]].copy()
    df_h8.dropna(subset=[col_genero, col_cafeina], inplace=True)

    # Filtrar para incluir apenas os códigos de gênero 1 (Masculino) e 2 (Feminino)
    df_h8 = df_h8[df_h8[col_genero].isin([1, 2])]

    if df_h8[col_genero].nunique() < 2:
        print("Não há pelo menos dois grupos de gênero (Masculino e Feminino) para comparar. Pulando análise.")
        return

    grupo_masculino = df_h8[df_h8[col_genero] == 1][col_cafeina]
    grupo_feminino = df_h8[df_h8[col_genero] == 2][col_cafeina]

    if grupo_masculino.empty or len(grupo_masculino) < 3:
        print(f"Grupo Masculino (GENERO_COD=1) não possui dados suficientes (N={len(grupo_masculino)}, min=3). Pulando H8.")
        return
    if grupo_feminino.empty or len(grupo_feminino) < 3:
        print(f"Grupo Feminino (GENERO_COD=2) não possui dados suficientes (N={len(grupo_feminino)}, min=3). Pulando H8.")
        return

    print(f"Grupo Masculino (N={len(grupo_masculino)}): Média Cafeína={grupo_masculino.mean():.2f} mg, DP={grupo_masculino.std():.2f} mg")
    print(f"Grupo Feminino (N={len(grupo_feminino)}): Média Cafeína={grupo_feminino.mean():.2f} mg, DP={grupo_feminino.std():.2f} mg")

    try:
        stat, p_valor = mannwhitneyu(grupo_masculino, grupo_feminino, alternative='two-sided')
        print(f"Teste Mann-Whitney U (bilateral): Estatística U={stat:.2f}, p-valor={p_valor:.4f}")
        if p_valor < 0.05:
            print("Resultado H8: Diferença estatisticamente significativa no consumo de cafeína entre gênero Masculino e Feminino.")
        else:
            print("Resultado H8: Nenhuma diferença estatisticamente significativa no consumo de cafeína entre gênero Masculino e Feminino.")
    except Exception as e:
        print(f"Erro ao executar o teste para H8: {e}")

def main():
    """Função principal para executar todas as análises."""
    # CAMINHO_CSV = '../IC_Dados_Processados.csv' # Ajuste o caminho conforme necessário
    CAMINHO_CSV = "IC_Dados_Processados.csv" # Usar caminho relativo à raiz do projeto
    df = carregar_dados(CAMINHO_CSV)

    if df.empty:
        print("DataFrame vazio. Encerrando análises.")
        return

    print("\n--- Verificação Inicial dos Dados para Análise ---")
    colunas_verificar = {
        'NIVEL_JOGADOR_COD': df['NIVEL_JOGADOR_COD'] if 'NIVEL_JOGADOR_COD' in df else None,
        'MG_CAFEINA_TOTAL_DIA': df['MG_CAFEINA_TOTAL_DIA'] if 'MG_CAFEINA_TOTAL_DIA' in df else None,
        'HORAS_JOGO_PRINCIPAL_MEDIA_DIA': df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'] if 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' in df else None,
        'EFEITO_ADVERSO_INSONIA_BIN': df['EFEITO_ADVERSO_INSONIA_BIN'] if 'EFEITO_ADVERSO_INSONIA_BIN' in df else None,
        'EFEITO_ADVERSO_NERVOSISMO_BIN': df['EFEITO_ADVERSO_NERVOSISMO_BIN'] if 'EFEITO_ADVERSO_NERVOSISMO_BIN' in df else None,
        'MELHORAR_PERFORMANCE_MOTIVO_BIN': df['MELHORAR_PERFORMANCE_MOTIVO_BIN'] if 'MELHORAR_PERFORMANCE_MOTIVO_BIN' in df else None,
        'PLATAFORMA_PRINCIPAL_COD': df['PLATAFORMA_PRINCIPAL_COD'] if 'PLATAFORMA_PRINCIPAL_COD' in df else None,
        'GENERO_COD': df['GENERO_COD'] if 'GENERO_COD' in df else None
    }
    for nome_col, dados_col in colunas_verificar.items():
        if dados_col is not None:
            print(f"Valores únicos em '{nome_col}': {dados_col.unique()[:10]} (primeiros 10 se houver muitos)")
            print(f"Tipos de dados da coluna '{nome_col}': {dados_col.dtype}")
            print(f"Presença de NaNs em '{nome_col}': {dados_col.isnull().sum()} / {len(df)}")
        else:
            print(f"Coluna '{nome_col}' não encontrada no DataFrame.")
    print("--------------------------------------------------")

    analisar_h1(df.copy())
    analisar_h2(df.copy())
    analisar_h3(df.copy())
    analisar_h7(df.copy())
    analisar_h6(df.copy())
    analisar_h8(df.copy()) # Adiciona a chamada para H8

if __name__ == '__main__':
    main()
    print("\n--- FIM DA EXECUÇÃO DO SCRIPT DE ANÁLISES INFERENCIAIS ---")
