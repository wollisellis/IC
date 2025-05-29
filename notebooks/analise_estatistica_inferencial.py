import pandas as pd
from scipy.stats import kruskal, mannwhitneyu, pearsonr, spearmanr
import statsmodels.api as sm
import os
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = "notebooks/outputs"
RESULTS_FILE = os.path.join(OUTPUT_DIR, "resultados_inferenciais.txt")
FIGURE_DIR = OUTPUT_DIR # Usar o mesmo diretório para figuras

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # FIGURE_DIR é o mesmo que OUTPUT_DIR, então não precisa criar separadamente se já foi criado.

def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    """Carrega os dados processados."""
    try:
        # Assumindo que a primeira linha é o cabeçalho
        df = pd.read_csv(caminho_csv, header=0) 
        print(f"Dados carregados com sucesso de {caminho_csv}")
        print(f"Shape do DataFrame: {df.shape}")
        
        # Conversão explícita para numérico, tratando erros
        colunas_numericas_chave = ['MG_CAFEINA_DIA', 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA']
        for col in colunas_numericas_chave:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                print(f"AVISO: Coluna numérica chave {col} não encontrada.")

        colunas_categoricas_chave = ['NIVEL_JOGADOR_COD'] 
        # Adicionar colunas de efeitos adversos se forem usadas
        # ex: 'EFEITO_ADVERSO_INSONIA_BIN', 'EFEITO_ADVERSO_NERVOSISMO_BIN', 'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD'
        
        for col_cat_key in ['EFEITO_ADVERSO_INSONIA_BIN', 'EFEITO_ADVERSO_NERVOSISMO_BIN', 'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD']:
            if col_cat_key in df.columns:
                colunas_categoricas_chave.append(col_cat_key)
                # Se forem binárias e não numéricas, converter
                if df[col_cat_key].dtype == 'object' and col_cat_key.endswith("_BIN"):
                     df[col_cat_key] = pd.to_numeric(df[col_cat_key], errors='coerce')


        for col in colunas_categoricas_chave:
            if col not in df.columns:
                print(f"AVISO: Coluna chave {col} não encontrada.")
            elif df[col].dtype == 'object' and col.endswith("_COD"): # Para colunas _COD que podem ser lidas como object
                 df[col] = pd.to_numeric(df[col], errors='coerce')


        return df
    except FileNotFoundError:
        print(f"ERRO: O arquivo {caminho_csv} não foi encontrado.")
        return pd.DataFrame()

def analisar_h1(df: pd.DataFrame, f):
    """
    H1: Jogadores de diferentes níveis (NIVEL_JOGADOR_COD) apresentam diferentes consumos de cafeína (MG_CAFEINA_DIA).
    Original: Jogadores profissionais consomem mais cafeína diariamente que amadores. (Testaremos diferença geral)
    """
    f.write("\\n--- Análise H1: Consumo de Cafeína (MG_CAFEINA_DIA) vs. Nível do Jogador (NIVEL_JOGADOR_COD) ---\\n")
    if 'MG_CAFEINA_DIA' not in df.columns or 'NIVEL_JOGADOR_COD' not in df.columns:
        f.write("Colunas necessárias para H1 (MG_CAFEINA_DIA, NIVEL_JOGADOR_COD) não encontradas. Pulando análise.\\n")
        print("Colunas necessárias para H1 não encontradas.")
        return

    df_h1 = df[['NIVEL_JOGADOR_COD', 'MG_CAFEINA_DIA']].copy()
    df_h1.dropna(inplace=True)

    if df_h1.empty:
        f.write("Não há dados suficientes para H1 após remover NaNs.\\n")
        print("Não há dados suficientes para H1 após remover NaNs.")
        return

    niveis_presentes = sorted(df_h1['NIVEL_JOGADOR_COD'].unique())
    f.write(f"Níveis de jogador encontrados (NIVEL_JOGADOR_COD): {niveis_presentes}\\n")

    map_nivel_jogador = {
        1: 'Amador/Casual',
        2: 'Semi-Profissional',
        3: 'Profissional'
    }

    grupos_para_teste = []
    nomes_dos_grupos = []

    for nivel_cod in niveis_presentes:
        nome_legivel = map_nivel_jogador.get(nivel_cod, f"Código {nivel_cod}")
        dados_do_grupo = df_h1[df_h1['NIVEL_JOGADOR_COD'] == nivel_cod]['MG_CAFEINA_DIA']
        if not dados_do_grupo.empty and len(dados_do_grupo) >= 5: # Mínimo de 5 observações por grupo
            grupos_para_teste.append(dados_do_grupo)
            nomes_dos_grupos.append(f"{nome_legivel} (Cód {nivel_cod})")
            f.write(f"Grupo '{nome_legivel} (Cód {nivel_cod})': N={len(dados_do_grupo)}, Média Cafeína={dados_do_grupo.mean():.2f} mg, DP={dados_do_grupo.std():.2f} mg\\n")
        else:
            f.write(f"Grupo '{nome_legivel} (Cód {nivel_cod})' com N={len(dados_do_grupo)} insuficiente para análise ou vazio após filtro.\\n")

    if len(grupos_para_teste) < 2:
        f.write("Não foi possível formar pelo menos dois grupos com dados suficientes para o teste H1.\\n")
        print("Não foi possível formar pelo menos dois grupos com dados suficientes para o teste H1.")
        return

    p_valor_h1 = 1.0
    try:
        if len(grupos_para_teste) == 2:
            stat, p_valor_h1 = mannwhitneyu(*grupos_para_teste, alternative='two-sided')
            f.write(f"Teste Mann-Whitney U entre '{nomes_dos_grupos[0]}' e '{nomes_dos_grupos[1]}': Estatística U={stat:.2f}, p-valor={p_valor_h1:.4f}\\n")
        elif len(grupos_para_teste) >= 3:
            stat, p_valor_h1 = kruskal(*grupos_para_teste)
            f.write(f"Teste Kruskal-Wallis entre os {len(nomes_dos_grupos)} grupos ({', '.join(nomes_dos_grupos)}): H-estatística={stat:.2f}, p-valor={p_valor_h1:.4f}\\n")
        
        if p_valor_h1 < 0.05:
            f.write("Resultado H1: Diferença estatisticamente significativa encontrada entre os grupos.\\n")
        else:
            f.write("Resultado H1: Nenhuma diferença estatisticamente significativa encontrada entre os grupos.\\n")
    except Exception as e:
        f.write(f"Erro ao executar o teste para H1: {e}\\n")
        print(f"Erro ao executar o teste para H1: {e}")

def analisar_h2(df: pd.DataFrame, f):
    """
    H2: Maior consumo de cafeína (MG_CAFEINA_DIA) está associado a maior tempo médio de jogo por dia (HORAS_JOGO_PRINCIPAL_MEDIA_DIA).
    """
    f.write("\\n--- Análise H2: Consumo de Cafeína (MG_CAFEINA_DIA) vs. Horas de Jogo (HORAS_JOGO_PRINCIPAL_MEDIA_DIA) ---\\n")
    if 'MG_CAFEINA_DIA' not in df.columns or 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' not in df.columns:
        f.write("Colunas necessárias para H2 (MG_CAFEINA_DIA, HORAS_JOGO_PRINCIPAL_MEDIA_DIA) não encontradas. Pulando.\\n")
        print("Colunas necessárias para H2 não encontradas.")
        return

    df_h2 = df[['MG_CAFEINA_DIA', 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA']].copy()
    df_h2.dropna(inplace=True)

    if df_h2.empty or len(df_h2) < 10: # Mínimo de 10 observações para correlação
        f.write(f"Não há dados suficientes para H2 após remover NaNs (mínimo 10, encontrados: {len(df_h2)}). Pulando.\\n")
        print(f"Não há dados suficientes para H2 (encontrados: {len(df_h2)}).")
        return

    cafeina = df_h2['MG_CAFEINA_DIA']
    horas_jogo = df_h2['HORAS_JOGO_PRINCIPAL_MEDIA_DIA']

    try:
        corr_spearman, p_spearman = spearmanr(cafeina, horas_jogo)
        f.write(f"Correlação de Spearman: rho={corr_spearman:.3f}, p-valor={p_spearman:.4f}, N={len(df_h2)}\\n")
        if p_spearman < 0.05:
            f.write("Resultado (Spearman) H2: Correlação estatisticamente significativa.\\n")
        else:
            f.write("Resultado (Spearman) H2: Nenhuma correlação estatisticamente significativa.\\n")
        
        # Gerar Figura 3: Diagrama de Dispersão
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='MG_CAFEINA_DIA', y='HORAS_JOGO_PRINCIPAL_MEDIA_DIA', data=df_h2, alpha=0.6)
        sns.regplot(x='MG_CAFEINA_DIA', y='HORAS_JOGO_PRINCIPAL_MEDIA_DIA', data=df_h2, scatter=False, color='red', ci=None, line_kws={'linestyle':'--'})
        plt.title('Figura 3: Consumo de Cafeína vs. Horas de Jogo')
        plt.xlabel('Consumo Diário de Cafeína (MG_CAFEINA_DIA)')
        plt.ylabel('Horas de Jogo Principal por Dia (HORAS_JOGO_PRINCIPAL_MEDIA_DIA)')
        plt.grid(True)
        fig3_path = os.path.join(FIGURE_DIR, "figura3_cafeina_vs_horas_jogo.png")
        plt.savefig(fig3_path)
        plt.close()
        f.write(f"Figura 3 salva em: {fig3_path}\n")
    except Exception as e:
        f.write(f"Erro ao calcular Correlação de Spearman para H2: {e}\\n")
        print(f"Erro ao calcular Correlação de Spearman para H2: {e}")

def analisar_h3(df: pd.DataFrame, f):
    """
    H3: Frequência de efeitos adversos (insônia, nervosismo) aumenta conforme a dose de cafeína (MG_CAFEINA_DIA).
    Adaptado: Se colunas binárias específicas não disponíveis, tentar com EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD.
    """
    f.write("\\n--- Análise H3: Efeitos Adversos vs. Dose de Cafeína (MG_CAFEINA_DIA) ---\\n")
    if 'MG_CAFEINA_DIA' not in df.columns:
        f.write("Coluna MG_CAFEINA_DIA não encontrada. Pulando H3.\\n")
        print("Coluna MG_CAFEINA_DIA não encontrada. Pulando H3.")
        return

    efeitos_binarios = {
        'EFEITO_ADVERSO_INSONIA_BIN': 'Insônia',
        'EFEITO_ADVERSO_NERVOSISMO_BIN': 'Nervosismo'
        # Adicionar outros efeitos binários se existirem e forem relevantes
    }
    
    h3_analisado = False
    for col_bin, nome_efeito in efeitos_binarios.items():
        if col_bin in df.columns:
            f.write(f"  Analisando efeito específico: {nome_efeito} (coluna: {col_bin})\\n")
            df_h3_bin = df[[col_bin, 'MG_CAFEINA_DIA']].copy()
            df_h3_bin.dropna(inplace=True)
            
            if df_h3_bin.empty:
                f.write(f"    Não há dados suficientes para {col_bin} após remover NaNs.\\n")
                continue
            
            if not pd.api.types.is_numeric_dtype(df_h3_bin[col_bin]) or not all(v in [0, 1] for v in df_h3_bin[col_bin].unique()):
                f.write(f"    Coluna {col_bin} não é binária (0 ou 1) ou não é numérica. Valores: {df_h3_bin[col_bin].unique()[:5]}. Pulando este efeito.\\n")
                continue

            grupo_com_efeito = df_h3_bin[df_h3_bin[col_bin] == 1]['MG_CAFEINA_DIA']
            grupo_sem_efeito = df_h3_bin[df_h3_bin[col_bin] == 0]['MG_CAFEINA_DIA']

            if grupo_com_efeito.empty or grupo_sem_efeito.empty or len(grupo_com_efeito) < 5 or len(grupo_sem_efeito) < 5:
                f.write(f"    Não há dados suficientes em ambos os grupos (COM e SEM {nome_efeito}, N_min=5) para o teste.\\n")
                f.write(f"      N_COM={len(grupo_com_efeito)}, N_SEM={len(grupo_sem_efeito)}\\n")
                continue
            
            f.write(f"    Grupo COM {nome_efeito} (N={len(grupo_com_efeito)}): Média Cafeína={grupo_com_efeito.mean():.2f} mg (DP={grupo_com_efeito.std():.2f}) mg\\n")
            f.write(f"    Grupo SEM {nome_efeito} (N={len(grupo_sem_efeito)}): Média Cafeína={grupo_sem_efeito.mean():.2f} mg (DP={grupo_sem_efeito.std():.2f}) mg\\n")

            try:
                # Teste unilateral: quem reporta efeito consome MAIS cafeína
                stat, p_valor = mannwhitneyu(grupo_com_efeito, grupo_sem_efeito, alternative='greater') 
                f.write(f"    Teste Mann-Whitney U (unilateral: COM {nome_efeito} > SEM {nome_efeito}): Estatística U={stat:.2f}, p-valor={p_valor:.4f}\\n")

                if p_valor < 0.05:
                    f.write(f"    Resultado H3 ({nome_efeito}): Consumo de cafeína é significativamente MAIOR no grupo COM {nome_efeito}.\\n")
                else:
                    f.write(f"    Resultado H3 ({nome_efeito}): Não há evidência de que o consumo de cafeína seja significativamente maior no grupo COM {nome_efeito}.\\n")
                h3_analisado = True
            except Exception as e:
                f.write(f"    Erro ao executar Mann-Whitney U para {nome_efeito}: {e}\\n")
                print(f"    Erro ao executar Mann-Whitney U para {nome_efeito}: {e}")
        else:
            f.write(f"  Coluna de efeito binário {col_bin} não encontrada.\\n")

    # Tentar com EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD se colunas binárias não foram analisadas
    if not h3_analisado and 'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD' in df.columns:
        f.write(f"  Analisando frequência geral de efeitos (EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD)\\n")
        col_freq = 'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD'
        
        df_h3_freq = df[[col_freq, 'MG_CAFEINA_DIA']].copy()
        df_h3_freq.dropna(inplace=True)

        if df_h3_freq.empty or len(df_h3_freq) < 10:
            f.write(f"    Não há dados suficientes para {col_freq} após remover NaNs (mínimo 10, encontrados: {len(df_h3_freq)}). Pulando.\\n")
        elif not pd.api.types.is_numeric_dtype(df_h3_freq[col_freq]):
            f.write(f"    Coluna {col_freq} não é numérica. Valores: {df_h3_freq[col_freq].unique()[:5]}. Pulando.\\n")
        else:
            frequencia_efeito = df_h3_freq[col_freq]
            cafeina = df_h3_freq['MG_CAFEINA_DIA']
            try:
                corr_spearman, p_spearman = spearmanr(cafeina, frequencia_efeito)
                f.write(f"    Correlação de Spearman entre MG_CAFEINA_DIA e {col_freq}: rho={corr_spearman:.3f}, p-valor={p_spearman:.4f}, N={len(df_h3_freq)}\\n")
                if p_spearman < 0.05:
                    f.write(f"    Resultado H3 (Frequência Geral): Correlação estatisticamente significativa.\\n")
                else:
                    f.write(f"    Resultado H3 (Frequência Geral): Nenhuma correlação estatisticamente significativa.\\n")
                h3_analisado = True
            except Exception as e:
                f.write(f"    Erro ao calcular Correlação de Spearman para {col_freq}: {e}\\n")
                print(f"    Erro ao calcular Correlação de Spearman para {col_freq}: {e}")
    
    if not h3_analisado:
        f.write("Não foi possível realizar a análise H3 com as colunas disponíveis ou dados suficientes.\\n")
        print("Não foi possível realizar a análise H3.")

def realizar_analises(df: pd.DataFrame, f):
    """Realiza as análises H1, H2, H3 e escreve os resultados no arquivo f."""
    f.write("--- Verificação Inicial dos Dados para Análise ---\\n")
    colunas_para_verificar = {
        'NIVEL_JOGADOR_COD': df['NIVEL_JOGADOR_COD'] if 'NIVEL_JOGADOR_COD' in df else None,
        'MG_CAFEINA_DIA': df['MG_CAFEINA_DIA'] if 'MG_CAFEINA_DIA' in df else None,
        'HORAS_JOGO_PRINCIPAL_MEDIA_DIA': df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'] if 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' in df else None,
        'EFEITO_ADVERSO_INSONIA_BIN': df['EFEITO_ADVERSO_INSONIA_BIN'] if 'EFEITO_ADVERSO_INSONIA_BIN' in df else None, # Será None se não existir
        'EFEITO_ADVERSO_NERVOSISMO_BIN': df['EFEITO_ADVERSO_NERVOSISMO_BIN'] if 'EFEITO_ADVERSO_NERVOSISMO_BIN' in df else None, # Será None se não existir
        'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD': df['EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD'] if 'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD' in df else None
    }

    for col, valor in colunas_para_verificar.items():
        if valor is not None:
            f.write(f"{col}: Valores únicos (primeiros 10 se houver muitos): {valor.unique()[:10]}\\n")
            f.write(f"{col}: Tipos de dados: {valor.dtype}\\n")
            if pd.api.types.is_numeric_dtype(valor):
                f.write(f"{col}: Presença de NaNs: {valor.isnull().sum()} / {len(valor)}\\n")
        else:
            f.write(f"AVISO IMPORTANTE: Coluna '{col}' NÃO encontrada no DataFrame.\\n")
    f.write("--------------------------------------------------\\n")

    analisar_h1(df, f)
    analisar_h2(df, f)
    analisar_h3(df, f)

if __name__ == '__main__':
    print(f"--- INÍCIO DA EXECUÇÃO DO SCRIPT DE ANÁLISES INFERENCIAIS ---")
    ensure_output_dir()
    
    # Caminho relativo ao root do projeto, onde o script é geralmente executado
    caminho_do_arquivo_csv = 'IC_Dados_Processados.csv' 
    df_processado = carregar_dados(caminho_do_arquivo_csv)

    if df_processado is not None:
        print(f"Shape do DataFrame após carregamento: {df_processado.shape}")
        with open(RESULTS_FILE, "w", encoding="utf-8") as f_out:
            f_out.write("Resultados das Análises Estatísticas Inferenciais\\n")
            f_out.write(f"Data da Análise: {pd.Timestamp.now()}\n")
            f_out.write(f"Arquivo de Dados: {os.path.basename(caminho_do_arquivo_csv)}\n")
            f_out.write(f"Shape do DataFrame Carregado: {df_processado.shape}\n\\n")
            realizar_analises(df_processado, f_out)
        print(f"Resultados salvos em: {RESULTS_FILE}")
    else:
        print("Não foi possível carregar os dados. Análises não realizadas.")
    
    print(f"--- FIM DA EXECUÇÃO DO SCRIPT DE ANÁLISES INFERENCIAIS ---") 