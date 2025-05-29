import pandas as pd
import numpy as np
from datetime import datetime
import re
import json

# Utility functions for extracting volume and dose values
def extract_vol_ml(text):
    """Extract numerical volume in ml from text; returns Int or NA if not found."""
    if pd.isna(text):
        return pd.NA
    text_str = str(text).lower()
    match = re.search(r'(\d+)\s*ml', text_str)
    if match:
        return int(match.group(1))
    return pd.NA


def extract_dose_mg(text):
    """Extract numerical dose in mg from text; returns Int or NA if not found."""
    if pd.isna(text):
        return pd.NA
    text_str = str(text).lower()
    match_mg = re.search(r'(\d+)\s*mg', text_str)
    if match_mg:
        return int(match_mg.group(1))
    match_num = re.search(r'(\d+)', text_str)
    if match_num:
        return int(match_num.group(1))
    return pd.NA


def load_data(path: str) -> pd.DataFrame:
    """Load CSV data from a file."""
    return pd.read_csv(path, encoding='utf-8', delimiter=',')


def filter_consent(df: pd.DataFrame) -> pd.DataFrame:
    """Filter participants who accepted TCLE and encode consent flag."""
    df = df[df['TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO (TCLE)'] == 'Aceito'].copy()
    df['TCLE_ACEITE'] = 1
    return df


def remove_pii(df: pd.DataFrame) -> pd.DataFrame:
    """Remove or drop PII columns from DataFrame."""
    return df.drop(columns=[
        'E-mail (para o envio do TCLE)',
        'Como você prefere ser chamado(a/e)?'
    ], errors='ignore')


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse timestamps and calculate age based on date of birth and latest response date."""
    # Standardize response timestamp
    df['TIMESTAMP_RESPOSTA'] = pd.to_datetime(df['Data'], errors='coerce')
    df['TIMESTAMP_RESPOSTA'] = df['TIMESTAMP_RESPOSTA'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # Reference date = most recent response
    latest = pd.to_datetime(df['Data'], errors='coerce').max()
    # Calculate age
    birth = pd.to_datetime(df['Data de Nascimento'], format='%d/%m/%Y', errors='coerce')
    df['IDADE'] = ((latest - birth).dt.days // 365).astype('Int64')
    return df


def clean_numeric_columns(df: pd.DataFrame, cols: dict) -> pd.DataFrame:
    """Clean numeric columns: replace decimal comma, handle '#ERROR!', convert to float."""
    for orig, new in cols.items():
        series = (
            df[orig]
            .astype(str)
            .str.replace(',', '.', regex=False)
            .replace({'#ERROR!': np.nan, '': np.nan})
        )
        df[new] = pd.to_numeric(series, errors='coerce')
    return df


def encode_column(df: pd.DataFrame, col: str, mapping: dict, new_col: str) -> pd.DataFrame:
    """Encode a categorical column using a mapping dict."""
    df[new_col] = (
        df[col]
        .astype(str)
        .str.strip()
        .map(mapping)
        .astype('Int64')
    )
    return df


def create_dummies(df: pd.DataFrame, column: str, prefix: str) -> pd.DataFrame:
    """Create dummy variables for multiple-choice text responses separated by commas."""
    col_data = df[column].dropna().str.split(',')
    categories = sorted({item.strip().lower() for sub in col_data for item in sub})
    for cat in categories:
        safe = cat.upper().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')
        dummy_col = f"{prefix}_{safe}"
        # Escape regex metacharacters in category
        pattern = r"\b" + re.escape(cat) + r"\b"
        df[dummy_col] = (
            df[column]
            .astype(str)
            .str.lower()
            .str.contains(pattern, na=False, regex=True)
            .astype('Int64')
        )
        df.loc[df[column].isna(), dummy_col] = pd.NA
    return df


def generate_codebook(df: pd.DataFrame, codebook_path: str) -> None:
    """Generate a detailed codebook from processed DataFrame."""
    with open(codebook_path, 'w', encoding='utf-8') as f:
        # Header
        f.write('VariableName\tType\tUniqueValues\n')
        for col in df.columns:
            dtype = str(df[col].dtype)
            # Capture unique values (convert to list)
            uniques = df[col].dropna().unique().tolist()
            # If too many unique values, sample first 20
            if len(uniques) > 20:
                uniques = uniques[:20] + ['...']
            # Serialize unique values as JSON string to preserve types
            uniques_str = json.dumps(uniques, ensure_ascii=False)
            f.write(f'{col}\t{dtype}\t"{uniques_str}"\n')


def export_processed(df: pd.DataFrame, csv_path: str, codebook_path: str) -> None:
    """Export processed DataFrame to CSV and generate a detailed codebook."""
    # Export CSV
    df.to_csv(csv_path, index=False, encoding='utf-8')
    # Generate codebook
    generate_codebook(df, codebook_path)


def process_all(input_path: str, output_csv: str, codebook_txt: str) -> pd.DataFrame:
    """Full pipeline: load, filter, clean, encode, and export dataset."""
    df = load_data(input_path)
    df = filter_consent(df)
    df = remove_pii(df)
    df = parse_dates(df)
    # Clean numeric columns
    numeric_map = {
        'Mg cafeína semana': 'MG_CAFEINA_SEMANA',
        'Mg cafeína dia': 'MG_CAFEINA_DIA',
        'Mg homens': 'MG_HOMENS',
        'Mg mulheres': 'MG_MULHERES'
    }
    df = clean_numeric_columns(df, numeric_map)
    # Encode categorical columns (add more mappings as needed)
    gender_map = {'Masculino': 1, 'Feminino': 2, 'Prefiro não responder': 3, 'Não-binário': 4}
    df = encode_column(df, 'Gênero', gender_map, 'GENERO_COD')
    # TODO: add other encodings following methodology

    # --- Início da Implementação Detalhada da Codificação ---

    # 2.5.2. Nível de educação -> NIVEL_EDUC_COD
    educ_map = {
        'Ensino médio completo': 1,
        'Ensino superior incompleto': 2,
        'Ensino superior completo': 3,
        'Pós-graduação': 4
    }
    df = encode_column(df, 'Nível de educação', educ_map, 'NIVEL_EDUC_COD')

    # 2.5.2. Em qual nível você se classifica como jogador de esportes eletrônicos? -> NIVEL_JOGADOR_COD
    player_level_map = {
        'Amador/Jogador casual': 1,
        'Semi-Profissional': 2,
        'Profissional': 3
    }
    df = encode_column(df, 'Em qual nível você se classifica como jogador de esportes eletrônicos?', player_level_map, 'NIVEL_JOGADOR_COD')

    # 2.5.2. Você consome café? -> CONSUMO_CAFE_BIN
    cafe_consum_map = {'Sim': 1, 'Não': 0}
    df = encode_column(df, 'Você consome café?', cafe_consum_map, 'CONSUMO_CAFE_BIN')

    # 2.5.2. Quantos dias por semana você consome café? -> CAFE_DIAS_SEMANA_NUM
    cafe_days_map = {
        'Raramente': 0.5,
        '1-2 vezes por semana': 1.5,
        '3-4 vezes por semana': 3.5,
        '5-6 vezes por semana': 5.5,
        'Todos os dias': 7,
        'Nunca': 0 # Adicionado conforme menção, embora não em IC_Dados_Curados
    }
    df['CAFE_DIAS_SEMANA_NUM'] = df['Quantos dias por semana você consome café?'].map(cafe_days_map)
    df.loc[df['CONSUMO_CAFE_BIN'] == 0, 'CAFE_DIAS_SEMANA_NUM'] = pd.NA # Se não consome café, NaN

    # 2.5.2. Em qual tipo de recipiente você costuma consumir seu café? -> CAFE_RECIPIENTE_VOL_ML & CAFE_RECIPIENTE_TIPO_COD
    df['CAFE_RECIPIENTE_VOL_ML'] = df['Em qual tipo de recipiente você costuma consumir seu café?'].apply(extract_vol_ml)
    
    recipiente_cafe_map = {
        'Xícara pequena: 50 ml': 1,
        'Xícara grande: 100 ml': 2,
        'Caneca média: 300 ml': 3,
        'Copo americano: 200 ml': 4,
        'Garrafa pequena: 500 ml': 5,
        'Cápsula (Café preparado usando máquinas que funcionam com cápsulas pré-preparadas)': 6
    }
    df = encode_column(df, 'Em qual tipo de recipiente você costuma consumir seu café?', recipiente_cafe_map, 'CAFE_RECIPIENTE_TIPO_COD')
    df.loc[df['CONSUMO_CAFE_BIN'] == 0, ['CAFE_RECIPIENTE_VOL_ML', 'CAFE_RECIPIENTE_TIPO_COD']] = pd.NA

    # 2.5.2. "Com base no recipiente que você selecionou anteriormente...", quantas vezes no dia...? -> CAFE_VEZES_DIA_NUM
    cafe_times_day_map = {
        '1 vez ao dia': 1,
        '2 vezes ao dia': 2,
        '3 vezes ao dia': 3,
        '4 vezes ao dia': 4,
        '5 vezes ou mais ao dia': 5
    }
    df['CAFE_VEZES_DIA_NUM'] = df['Com base no recipiente que você selecionou anteriormente ( ___ "), quantas vezes no dia você consome café nesse recipiente?'].map(cafe_times_day_map)
    df.loc[df['CONSUMO_CAFE_BIN'] == 0, 'CAFE_VEZES_DIA_NUM'] = pd.NA
    
    # 2.5.2. Qual tipo de café você mais costuma consumir? -> CAFE_TIPO_PRINCIPAL_COD
    cafe_type_map = {
        'Coado (Café filtrado através de um coador de papel ou pano)': 1,
        'Expresso (Café forte e concentrado, feito sob alta pressão)': 2,
        'Instantâneo (Café em pó que dissolve em água quente)': 3,
        'Cápsula (Café preparado usando máquinas que funcionam com cápsulas pré-preparadas)': 4,
        'Café com leite (como latte, cappuccino, macchiato)': 5,
        'Frappuccino (Bebida gelada à base de café, com chantilly)': 6,
        'Descafeinado (Café sem cafeína)': 7, # Conforme RelatórioFinal_Éllis.md
        'Outro': 8 # Conforme RelatórioFinal_Éllis.md
    }
    df = encode_column(df, 'Qual tipo de café você mais costuma consumir?', cafe_type_map, 'CAFE_TIPO_PRINCIPAL_COD')
    df.loc[df['CONSUMO_CAFE_BIN'] == 0, 'CAFE_TIPO_PRINCIPAL_COD'] = pd.NA

    # 2.5.2. "Quantas horas por dia, em média, você joga e-sports?" (primeira ocorrência) -> HORAS_JOGO_PRINCIPAL_MEDIA_DIA
    # 2.5.2. "Quantas horas por dia, em média, você joga e-sports?" (segunda ocorrência) -> HORAS_JOGO_OUTROS_MEDIA_DIA
    game_hours_map = {
        'Menos de 1 hora': 0.5,
        '1-2 horas': 1.5,
        '2-4 horas': 3.0,  # Média de 2 e 4
        '4-6 horas': 5.0,  # Média de 4 e 6
        'Mais de 6 horas': 7.0 # Estimativa conservadora, pode ser ajustada
    }
    df['HORAS_JOGO_PRINCIPAL_MEDIA_DIA'] = df['Quantas horas por dia, em média, você joga e-sports?'].map(game_hours_map)
    # A segunda coluna de horas de jogo é nomeada com ".1" pelo pandas
    df['HORAS_JOGO_OUTROS_MEDIA_DIA'] = df['Quantas horas por dia, em média, você joga e-sports?.1'].map(game_hours_map)
    
    # 2.5.2. Suplemento: Qual a dose que você toma de cafeína em suplemento por dia? -> SUPLEM_DOSE_CAFEINA_MG
    df['SUPLEM_DOSE_CAFEINA_MG'] = df['Qual a dose que você toma de cafeína em suplemento por dia?'].apply(extract_dose_mg)

    # 2.5.2. Suplemento: "No dia que você costuma consumir ___", quantas vezes você toma essa porção? -> SUPLEM_DOSES_NUM
    # Esta pergunta no CSV original parece ser "Quantos dias na semana você consome suplemento com cafeína?"
    # E "Em quais momentos do dia você costuma consumir o seu suplemento?"
    # O roadmap menciona SUPLEM_DOSES_NUM. A pergunta mais próxima de "doses por dia" é
    # "Qual a dose que você toma de cafeína em suplemento por dia?" se interpretada como "uma dose de X mg"
    # ou "Quantos dias na semana...", que parece mais frequência semanal.
    # Vou assumir que SUPLEM_DOSES_NUM se refere a "quantas vezes ao dia toma essa dose", mas não há uma pergunta direta para isso.
    # A coluna "Qual a dose que você toma de cafeína em suplemento por dia?" pode implicar uma única dose diária
    # de X mg nos dias de consumo.
    # Para SUPLEM_DOSES_NUM, vou usar uma lógica placeholder e marcar para revisão.
    # Se "Qual a dose que você toma de cafeína em suplemento por dia?" for "200mg duas vezes ao dia", precisaria de parsing mais complexo.
    # Por ora, se SUPLEM_DOSE_CAFEINA_MG > 0, SUPLEM_DOSES_NUM = 1 (assumindo uma dose daquela quantidade nos dias de uso).
    df['SUPLEM_DOSES_NUM'] = pd.NA
    df.loc[df['SUPLEM_DOSE_CAFEINA_MG'].notna() & (df['SUPLEM_DOSE_CAFEINA_MG'] > 0), 'SUPLEM_DOSES_NUM'] = 1
    # Se a pessoa não consome suplemento (pergunta "Você consome algum suplemento que contenha cafeína?")
    # então SUPLEM_DOSE_CAFEINA_MG e SUPLEM_DOSES_NUM devem ser NaN.
    # Adicionaremos essa lógica quando a coluna de consumo de suplemento for codificada.

    # 2.5.2. Em que estado você reside? -> ESTADO_RESIDENCIA_COD
    # Criar mapeamento extenso de estados brasileiros para códigos numéricos.
    # Exemplo simplificado (expandir com todos os estados e DF)
    estado_map = {
        'São Paulo': 1, 'Rio de Janeiro': 2, 'Minas Gerais': 3, 'Distrito Federal': 4,
        'Alagoas': 5, 'Ceará': 6, 'Bahia': 7, 'Paraná': 8, 'Santa Catarina': 9,
        'Pernambuco': 10, 'Paraíba': 11, 'Espirito Santo': 12, # Corrigido "Espirito Santo"
        # Adicionar outros estados conforme aparecem nos dados e no relatório
    }
    # Assegurar que a coluna existe antes de tentar acessá-la
    if 'Em que estado você reside?' in df.columns:
        df = encode_column(df, 'Em que estado você reside?', estado_map, 'ESTADO_RESIDENCIA_COD')
    else:
        df['ESTADO_RESIDENCIA_COD'] = pd.NA # Criar coluna com NA se a original não existir

    # 2.5.2. Em qual cidade você reside? -> CIDADE_RESIDENCIA_PREENCHIDO
    # Criar flag binária: 1 se preenchido, 0 se NaN/vazio, NA se a coluna original não existir
    if 'Em qual cidade você reside?' in df.columns:
        df['CIDADE_RESIDENCIA_PREENCHIDO'] = df['Em qual cidade você reside?'].notna() & (df['Em qual cidade você reside?'].str.strip() != '')
        df['CIDADE_RESIDENCIA_PREENCHIDO'] = df['CIDADE_RESIDENCIA_PREENCHIDO'].astype(int)
        df.loc[df['Em qual cidade você reside?'].isna(), 'CIDADE_RESIDENCIA_PREENCHIDO'] = pd.NA # Propagar NA
    else:
        df['CIDADE_RESIDENCIA_PREENCHIDO'] = pd.NA


    # 2.5.2. Ocupação profissional -> OCUPACAO_COD
    # Alta cardinalidade. Usar mapeamento do RelatórioFinal_Éllis.md.
    # Exemplo inicial de mapeamento (deve ser expandido e refinado conforme o relatório):
    ocupacao_map = {
        'Estudante': 1,
        'Streamer': 2,
        'estudante': 1, # Normalizar caixa
        'Psicólogo': 3,
        'Designer de Moda': 4,
        'Empresário e Contabilista': 5, # Considerar agrupar ou manter separado
        'Jornalista': 6,
        'Empreendedor': 5, # Agrupar com Empresário?
        'Estagiário de Marketing': 7, # Ou agrupar com Estagiário?
        'Gerente de Marketing': 8,
        'Empresário': 5,
        'Servidor Público': 9,
        'Gestor de TI': 10,
        'Redator de esports': 11,
        'Micro Empreendedor': 5, # Agrupar?
        'Bolsista de pesquisa': 1, # Ou categoria própria?
        'Editora de vídeo (freelancer)': 12,
        'Bartender': 13,
        'Psicóloga': 3, # Agrupar com Psicólogo
        'Aluna de doutorado': 1, # Agrupar com Estudante
        'Pesquisadora': 1, # Agrupar com Estudante ou Bolsista?
        'Auxiliar de loja': 14,
        'Engenheira Civil': 15,
        'Coordenadora de Marketing': 8, # Agrupar com Gerente?
        'Community Manager': 16,
        'Desenvolvedor': 17,
        'Personal Trainer': 18,
        'Profissional de educação física': 19, # Ou agrupar com Personal Trainer?
        'Engenheiro de dados': 17, # Agrupar com Desenvolvedor?
        'CEO': 5, # Agrupar com Empresário?
        'bancário': 20,
        'Designer Gráfico': 21,
        'Desempregada': 22,
        'Nutricionista': 23,
        'Estagiário': 7,
        'Bancária': 20, # Agrupar
        'instrutora de idiomas': 24,
        'freelancer': 12, # Agrupar com Editora de vídeo (freelancer)?
        'desempregado': 22, # Agrupar
        'Sorveteiro': 25,
        'Publicitária': 26,
        'ESTUDANTE': 1, # Normalizar
        'Secretario': 27,
        'Estagiário Administrativo': 7, # Agrupar
        'Estudante/Pesquisador/Autônomo': 1, # Mapeamento complexo, priorizar Estudante ou criar nova?
        # Adicionar outras ocupações e seus códigos conforme RelatórioFinal_Éllis.md
        # Tratar "Outro" e valores não mapeados explicitamente como NaN ou um código específico para "Não especificado/Outro"
    }
    # Normalizar texto antes de mapear para melhorar a correspondência
    if 'Ocupação profissional' in df.columns:
        df['OCUPACAO_NORMALIZADA'] = df['Ocupação profissional'].astype(str).str.lower().str.strip()
        df = encode_column(df, 'OCUPACAO_NORMALIZADA', ocupacao_map, 'OCUPACAO_COD')
        df.drop(columns=['OCUPACAO_NORMALIZADA'], inplace=True, errors='ignore') # Limpar coluna temporária
        # Se após o mapeamento ainda houver NaNs onde a original não era NaN, pode indicar uma ocupação não mapeada.
        # No esquema atual da encode_column, eles viram Int64 NA.
    else:
        df['OCUPACAO_COD'] = pd.NA

    # 2.5.2. Você compete ou já competiu em campeonatos de esportes eletrônicos? -> COMPETIU_CAMPEONATOS_BIN
    competed_map = {
        'Sim': 1,
        'Não': 0
    }
    if 'Você compete ou já competiu em campeonatos de esportes eletrônicos?' in df.columns:
        df = encode_column(df, 'Você compete ou já competiu em campeonatos de esportes eletrônicos?', competed_map, 'COMPETIU_CAMPEONATOS_BIN')
    else:
        df['COMPETIU_CAMPEONATOS_BIN'] = pd.NA

    # 2.5.2. Em qual plataforma você mais joga? -> PLATAFORMA_PRINCIPAL_COD
    platform_map = {
        'PC': 1,
        'Mobile/Celular': 2,
        'PlayStation': 3,
        'Xbox': 4,
        'Nintendo': 5,
        'Outra': 6 # Conforme RelatórioFinal_Éllis.md
    }
    if 'Em qual plataforma você mais joga?' in df.columns:
        df = encode_column(df, 'Em qual plataforma você mais joga?', platform_map, 'PLATAFORMA_PRINCIPAL_COD')
    else:
        df['PLATAFORMA_PRINCIPAL_COD'] = pd.NA

    # 2.5.2. Qual é o seu jogo eletrônico principal? -> JOGO_PRINCIPAL_COD
    # Alta cardinalidade. Usar mapeamento do RelatórioFinal_Éllis.md.
    # Exemplo MUITO simplificado. VOCÊ DEVE EXPANDIR ISTO DETALHADAMENTE.
    main_game_map = {
        'league of legends': 1, # Exemplo, normalizar para lower
        'valorant': 2,
        'counter-strike: global offensive': 3,
        'counter-strike': 3, # Agrupar CSs?
        'apex legends': 4,
        'fortnite': 5,
        # ... adicione todos os jogos e seus códigos do seu relatório aqui
    }
    if 'Qual é o seu jogo eletrônico principal?' in df.columns:
        df['JOGO_PRINCIPAL_NORMALIZADO'] = df['Qual é o seu jogo eletrônico principal?'].astype(str).str.lower().str.strip()
        df = encode_column(df, 'JOGO_PRINCIPAL_NORMALIZADO', main_game_map, 'JOGO_PRINCIPAL_COD')
        df.drop(columns=['JOGO_PRINCIPAL_NORMALIZADO'], inplace=True, errors='ignore')
    else:
        df['JOGO_PRINCIPAL_COD'] = pd.NA

    # 2.5.2. Há quanto tempo você joga esse jogo? -> TEMPO_JOGO_PRINCIPAL_COD
    time_playing_map = {
        'Menos de 6 meses': 1,
        'Entre 6 meses e 1 ano': 2,
        'Entre 1 ano e 2 anos': 3,
        'Entre 2 anos e 5 anos': 4,
        'Entre 5 anos e 10 anos': 5,
        'Mais de 10 anos': 6
    }
    if 'Há quanto tempo você joga esse jogo?' in df.columns:
        df = encode_column(df, 'Há quanto tempo você joga esse jogo?', time_playing_map, 'TEMPO_JOGO_PRINCIPAL_COD')
    else:
        df['TEMPO_JOGO_PRINCIPAL_COD'] = pd.NA

    # 2.5.2. Você faz parte de algum time ou organização de esportes eletrônicos? -> PARTE_TIME_ORG_BIN
    team_org_map = {
        # A coluna original tem "Sim", "Não faço", "Não" e nomes de times.
        # Precisa de uma função customizada para tratar isso.
        # O objetivo é PARTE_TIME_ORG_BIN (1 se sim/nome do time, 0 se Não/Não faço)
        # e NOME_TIME_ORG_PREENCHIDO_BIN (1 se nome do time, 0 se Sim/Não/Não faço)
    }
    # Implementação para PARTE_TIME_ORG_BIN e NOME_TIME_ORG_PREENCHIDO_BIN
    col_team_org = 'Você faz parte de algum time ou organização de esportes eletrônicos?'
    if col_team_org in df.columns:
        # PARTE_TIME_ORG_BIN
        # Considera 'Sim' ou qualquer texto que não seja 'Não' ou 'Não faço' como 1
        def map_parte_time(value):
            if pd.isna(value): return pd.NA
            val_lower = str(value).lower().strip()
            if val_lower in ['não', 'nao', 'não faço', 'nao faco', '']: return 0
            return 1 # Se preenchido com 'Sim' ou nome do time
        df['PARTE_TIME_ORG_BIN'] = df[col_team_org].apply(map_parte_time).astype('Int64')

        # NOME_TIME_ORG_PREENCHIDO_BIN
        # Considera 1 apenas se for um nome de time (não 'Sim', 'Não', 'Não faço')
        def map_nome_time_preenchido(value):
            if pd.isna(value): return pd.NA
            val_lower = str(value).lower().strip()
            # Lista de respostas que indicam ausência de nome de time ou resposta genérica "sim"
            non_team_names = ['sim', 'não', 'nao', 'não faço', 'nao faco', ''] 
            if val_lower in non_team_names: return 0
            return 1 # Se for um texto e não estiver na lista acima, é um nome de time
        df['NOME_TIME_ORG_PREENCHIDO_BIN'] = df[col_team_org].apply(map_nome_time_preenchido).astype('Int64')
    else:
        df['PARTE_TIME_ORG_BIN'] = pd.NA
        df['NOME_TIME_ORG_PREENCHIDO_BIN'] = pd.NA

    # 2.5.2. "Além do tipo de café selecionado anteriormente, você costuma consumir outro tipo...?" -> CAFE_CONSUMO_OUTRO_TIPO_COD
    # A pergunta original é "Além do tipo de café selecionado anteriormente, você costuma consumir outro tipo no mesmo dia ou tem a frequência de alternar ao longo dos dias?"
    # Respostas parecem ser qualitativas sobre o HÁBITO de variar.
    # O RelatórioFinal_Éllis.md deve guiar a codificação exata.
    # Exemplo de mapeamento, PRECISA SER VALIDADO E COMPLETADO conforme o relatório:
    cafe_outro_tipo_map = {
        'Geralmente consumo o mesmo tipo de café': 0,
        'Alterno entre os dias (um dia tomo um tipo, outro dia tomo outro)': 1,
        'Tomo mais de 1 tipo de café por dia': 2,
        'Raramente consumo outro tipo': 3 # Suposição, verificar no relatório
        # Adicionar outras respostas e seus códigos
    }
    col_cafe_outro = 'Além do tipo de café selecionado anteriormente, você costuma consumir outro tipo no mesmo dia ou tem a frequência de alternar ao longo dos dias?'
    if col_cafe_outro in df.columns:
        df = encode_column(df, col_cafe_outro, cafe_outro_tipo_map, 'CAFE_CONSUMO_OUTRO_TIPO_COD')
        df.loc[df['CONSUMO_CAFE_BIN'] == 0, 'CAFE_CONSUMO_OUTRO_TIPO_COD'] = pd.NA # Se não consome café, NaN
    else:
        df['CAFE_CONSUMO_OUTRO_TIPO_COD'] = pd.NA

    # 2.5.2. Você consome energéticos? -> CONSUMO_ENERGETICOS_BIN
    energetico_consumo_map = {'Sim': 1, 'Não': 0}
    if 'Você consome energéticos?' in df.columns:
        df = encode_column(df, 'Você consome energéticos?', energetico_consumo_map, 'CONSUMO_ENERGETICOS_BIN')
    else:
        df['CONSUMO_ENERGETICOS_BIN'] = pd.NA

    # 2.5.2. Quantos dias por semana você consome energético? -> ENERGETICO_DIAS_SEMANA_NUM
    energetico_days_map = {
        'Raramente': 0.5,
        '1-2 vezes por semana': 1.5,
        '3-4 vezes por semana': 3.5,
        '5-6 vezes por semana': 5.5,
        'Todos os dias': 7,
        'Nunca': 0 # Adicionado para consistência, verificar se aparece nos dados
    }
    if 'Quantos dias por semana você consome energético?' in df.columns:
        df['ENERGETICO_DIAS_SEMANA_NUM'] = df['Quantos dias por semana você consome energético?'].map(energetico_days_map)
        df.loc[df['CONSUMO_ENERGETICOS_BIN'] == 0, 'ENERGETICO_DIAS_SEMANA_NUM'] = pd.NA
    else:
        df['ENERGETICO_DIAS_SEMANA_NUM'] = pd.NA

    # 2.5.2. Qual tipo de energético você mais costuma consumir? -> ENERGETICO_TIPO_PRINCIPAL_COD
    # Exemplo de mapeamento - EXPANDIR E VALIDAR com RelatórioFinal_Éllis.md e dados!
    energetico_type_map = {
        'Red Bull': 1,
        'Monster': 2,
        'TNT': 3,
        'Flying Horse': 4,
        'Baly': 5,
        'Outro': 99 # Código para outros, se necessário
    }
    col_energetico_tipo = 'Qual tipo de energético você mais costuma consumir?'
    if col_energetico_tipo in df.columns:
        # Normalizar antes de mapear, pois nomes podem ter variações
        df['ENERGETICO_TIPO_NORMALIZADO'] = df[col_energetico_tipo].astype(str).str.lower().str.strip()
        # Aplica o mapeamento. encode_column já lida comastype('Int64').
        df = encode_column(df, 'ENERGETICO_TIPO_NORMALIZADO', energetico_type_map, 'ENERGETICO_TIPO_PRINCIPAL_COD')
        df.drop(columns=['ENERGETICO_TIPO_NORMALIZADO'], inplace=True, errors='ignore')
        df.loc[df['CONSUMO_ENERGETICOS_BIN'] == 0, 'ENERGETICO_TIPO_PRINCIPAL_COD'] = pd.NA
    else:
        df['ENERGETICO_TIPO_PRINCIPAL_COD'] = pd.NA

    # 2.5.2. Qual o tamanho da lata ou recipiente do ___ que você costuma consumir? -> ENERGETICO_TAMANHO_RECIPIENTE_COD e ENERGETICO_TAMANHO_RECIPIENTE_ML_NUM
    col_energetico_recipiente = 'Qual o tamanho da lata ou recipiente do ___ que você costuma consumir?'
    if col_energetico_recipiente in df.columns:
        df['ENERGETICO_TAMANHO_RECIPIENTE_ML_NUM'] = df[col_energetico_recipiente].apply(extract_vol_ml) # Reutiliza função do café
        
        # Exemplo de mapeamento para ENERGETICO_TAMANHO_RECIPIENTE_COD - VALIDAR E EXPANDIR!
        energetico_recipiente_map = {
            'Pequeno (aprox, 250ml)': 1,
            'Médio (aprox, 355ml)': 2, # Ex: Red Bull 355ml, Monster antigo?
            'Grande (aprox, 473ml)': 3, # Ex: Monster 473ml/500ml
            'Outro': 99
        }
        # Para o COD, podemos mapear o texto original após normalização
        df['ENERGETICO_RECIPIENTE_NORMALIZADO'] = df[col_energetico_recipiente].astype(str).str.lower().str.strip()
        # Remover parenteses e conteúdo para melhorar matching se necessário, ou mapear direto
        # Ex: 'pequeno (aprox, 250ml)' -> 1
        # Este mapeamento direto pode ser mais robusto se as strings forem consistentes
        df = encode_column(df, 'ENERGETICO_RECIPIENTE_NORMALIZADO', energetico_recipiente_map, 'ENERGETICO_TAMANHO_RECIPIENTE_COD')
        df.drop(columns=['ENERGETICO_RECIPIENTE_NORMALIZADO'], inplace=True, errors='ignore')

        df.loc[df['CONSUMO_ENERGETICOS_BIN'] == 0, ['ENERGETICO_TAMANHO_RECIPIENTE_ML_NUM', 'ENERGETICO_TAMANHO_RECIPIENTE_COD']] = pd.NA
    else:
        df['ENERGETICO_TAMANHO_RECIPIENTE_ML_NUM'] = pd.NA
        df['ENERGETICO_TAMANHO_RECIPIENTE_COD'] = pd.NA

    # 2.5.2. "No dia que você costuma consumir energético, quantas vezes você toma essa porção ___?" -> ENERGETICO_VEZES_DIA_NUM
    energetico_times_day_map = {
        '1 vez ao dia': 1,
        '2 vezes ao dia': 2,
        '3 vezes ao dia': 3,
        '4 vezes ao dia': 4,
        '5 vezes ou mais ao dia': 5
    }
    col_energetico_vezes_dia = 'No dia que você costuma consumir energético, quantas vezes você toma essa porção ___?'
    if col_energetico_vezes_dia in df.columns:
        df['ENERGETICO_VEZES_DIA_NUM'] = df[col_energetico_vezes_dia].map(energetico_times_day_map)
        df.loc[df['CONSUMO_ENERGETICOS_BIN'] == 0, 'ENERGETICO_VEZES_DIA_NUM'] = pd.NA
    else:
        df['ENERGETICO_VEZES_DIA_NUM'] = pd.NA

    # --- Consumo de Chá ---
    # 2.5.2. Você consome chá? -> CONSUMO_CHA_BIN
    cha_consumo_map = {'Sim': 1, 'Não': 0}
    if 'Você consome chá?' in df.columns:
        df = encode_column(df, 'Você consome chá?', cha_consumo_map, 'CONSUMO_CHA_BIN')
    else:
        df['CONSUMO_CHA_BIN'] = pd.NA

    # 2.5.2. Quantos dias por semana você consome chá? -> CHA_DIAS_SEMANA_NUM
    cha_days_map = {
        'Raramente': 0.5,
        '1-2 vezes por semana': 1.5,
        '3-4 vezes por semana': 3.5,
        '5-6 vezes por semana': 5.5,
        'Todos os dias': 7,
        'Nunca': 0
    }
    if 'Quantos dias por semana você consome chá?' in df.columns:
        df['CHA_DIAS_SEMANA_NUM'] = df['Quantos dias por semana você consome chá?'].map(cha_days_map)
        df.loc[df['CONSUMO_CHA_BIN'] == 0, 'CHA_DIAS_SEMANA_NUM'] = pd.NA
    else:
        df['CHA_DIAS_SEMANA_NUM'] = pd.NA

    # 2.5.2. Qual tipo de chá você mais consome? -> CHA_TIPO_PRINCIPAL_COD
    # Exemplo de mapeamento - EXPANDIR E VALIDAR com RelatórioFinal_Éllis.md e dados!
    cha_type_map = {
        'chá preto': 1, # Normalizar para lower case
        'chá verde': 2,
        'chá mate': 3,
        'chá de ervas (ex: camomila, hortelã, boldo, capim-limão, hibisco, erva-doce)': 4,
        'chá de frutas (ex: maracujá, amora, morango,,)': 5, # Atenção à vírgula dupla
        'chá gelado (ice tea)': 6,
        'chá oolong': 7,
        'chimarrão': 8, # Embora tecnicamente não seja chá, pode estar agrupado aqui
        'outro': 99
    }
    col_cha_tipo = 'Qual tipo de chá você mais consome?'
    if col_cha_tipo in df.columns:
        df['CHA_TIPO_NORMALIZADO'] = df[col_cha_tipo].astype(str).str.lower().str.strip().str.replace(',,', ',', regex=False)
        df = encode_column(df, 'CHA_TIPO_NORMALIZADO', cha_type_map, 'CHA_TIPO_PRINCIPAL_COD')
        df.drop(columns=['CHA_TIPO_NORMALIZADO'], inplace=True, errors='ignore')
        df.loc[df['CONSUMO_CHA_BIN'] == 0, 'CHA_TIPO_PRINCIPAL_COD'] = pd.NA
    else:
        df['CHA_TIPO_PRINCIPAL_COD'] = pd.NA

    # 2.5.2. Em qual tipo de recipiente você costuma consumir seu chá? -> CHA_RECIPIENTE_COD e CHA_RECIPIENTE_VOL_ML_NUM
    col_cha_recipiente = 'Em qual tipo de recipiente você costuma consumir seu chá?'
    if col_cha_recipiente in df.columns:
        df['CHA_RECIPIENTE_VOL_ML_NUM'] = df[col_cha_recipiente].apply(extract_vol_ml) # Reutiliza função
        
        # Exemplo de mapeamento para CHA_RECIPIENTE_COD - VALIDAR E EXPANDIR!
        cha_recipiente_map = {
            'xícara pequena: 50 ml': 1,
            'xícara grande: 100 ml': 2,
            'caneca média: 300 ml': 3,
            'copo americano: 200 ml': 4,
            'garrafa pequena: 500 ml': 5,
            'outro': 99
        }
        df['CHA_RECIPIENTE_NORMALIZADO'] = df[col_cha_recipiente].astype(str).str.lower().str.strip()
        df = encode_column(df, 'CHA_RECIPIENTE_NORMALIZADO', cha_recipiente_map, 'CHA_RECIPIENTE_COD')
        df.drop(columns=['CHA_RECIPIENTE_NORMALIZADO'], inplace=True, errors='ignore')
        df.loc[df['CONSUMO_CHA_BIN'] == 0, ['CHA_RECIPIENTE_VOL_ML_NUM', 'CHA_RECIPIENTE_COD']] = pd.NA
    else:
        df['CHA_RECIPIENTE_VOL_ML_NUM'] = pd.NA
        df['CHA_RECIPIENTE_COD'] = pd.NA

    # 2.5.2. "Com base no recipiente que você selecionou anteriormente ( ___ ), quantas vezes ao dia você consome chá...?" -> CHA_VEZES_DIA_NUM
    cha_times_day_map = {
        '1 vez ao dia': 1,
        '2 vezes ao dia': 2,
        '3 vezes ao dia': 3,
        '4 vezes ao dia': 4,
        '5 vezes ou mais ao dia': 5
    }
    col_cha_vezes_dia = 'Com base no recipiente que você selecionou anteriormente ( ___ ), quantas vezes ao dia você consome chá nesse recipiente?'
    if col_cha_vezes_dia in df.columns:
        df['CHA_VEZES_DIA_NUM'] = df[col_cha_vezes_dia].map(cha_times_day_map)
        df.loc[df['CONSUMO_CHA_BIN'] == 0, 'CHA_VEZES_DIA_NUM'] = pd.NA
    else:
        df['CHA_VEZES_DIA_NUM'] = pd.NA

    # --- Consumo de Chocolate ---
    # 2.5.2. Especifique a porção média de chocolate no dia que consome ( ___ ) -> CHOCOLATE_PORCAO_COD
    # Esta é uma coluna de texto livre. O mapeamento precisa ser definido com base no RelatórioFinal_Éllis.md e nos dados.
    # Exemplo de mapeamento - SUBSTITUIR/EXPANDIR CONFORME SEU RELATÓRIO!
    chocolate_porcao_map = {
        '2 quadradinhos(20g)': 1,
        '1 barra pequena': 2,
        '3-4 quadradinhos': 3,
        '1 barra': 4,
        '4 quadrados': 3, # Agrupar com 3-4 quadradinhos?
        '1 unidade (média de 50g)': 5,
        'meia barra pequena': 6,
        '5 quadradinhos': 7,
        # ... Adicionar todas as variações e seus códigos
        'outro': 99
    }
    col_chocolate_porcao = 'Especifique a porção média de chocolate no dia que consome ( ___ )'
    if col_chocolate_porcao in df.columns:
        # Normalizar para minúsculas e remover espaços para ajudar no mapeamento
        df['CHOCOLATE_PORCAO_NORMALIZADA'] = df[col_chocolate_porcao].astype(str).str.lower().str.strip()
        df = encode_column(df, 'CHOCOLATE_PORCAO_NORMALIZADA', chocolate_porcao_map, 'CHOCOLATE_PORCAO_COD')
        df.drop(columns=['CHOCOLATE_PORCAO_NORMALIZADA'], inplace=True, errors='ignore')
        # Adicionar lógica para CONSUMO_CHOCOLATE_BIN se necessário, e condicionar esta codificação a ele.
        # Por ora, se não houver consumo de chocolate (variável a ser criada), esta coluna deve ser NaN.
    else:
        df['CHOCOLATE_PORCAO_COD'] = pd.NA

    # --- Motivo do Consumo de Cafeína ---
    # Pergunta: Você consome cafeína pensando em melhorar a sua performance nos esportes eletrônicos? -> MELHORAR_PERFORMANCE_MOTIVO_BIN
    col_melhorar_performance = 'Você consome cafeína pensando em melhorar a sua performance nos esportes eletrônicos?'
    if col_melhorar_performance in df.columns:
        performance_map = {'Sim': 1, 'Não': 0}
        df = encode_column(df, col_melhorar_performance, performance_map, 'MELHORAR_PERFORMANCE_MOTIVO_BIN')
    else:
        df['MELHORAR_PERFORMANCE_MOTIVO_BIN'] = pd.NA
        df['MELHORAR_PERFORMANCE_MOTIVO_BIN'] = df['MELHORAR_PERFORMANCE_MOTIVO_BIN'].astype('Int64')

    # --- Efeitos Adversos ---
    # Pergunta original sobre ter sentido ou não ALGUM efeito:
    col_efeitos_adv_geral_raw = "Você já experimentou algum dos seguintes efeitos adversos após consumir cafeína?Insônia, taquicardia (coração acelerado), nervosismo, tremores, dor no estômago ou outro sintoma"
    
    df['EFEITO_ADVERSO_PRESENTE_BIN'] = pd.NA # Inicializar a coluna
    if col_efeitos_adv_geral_raw in df.columns:
        sim_nao_map = {'sim': 1, 'não': 0, 'nao': 0}
        df['EFEITO_ADVERSO_PRESENTE_BIN'] = df[col_efeitos_adv_geral_raw].astype(str).str.lower().str.strip().map(sim_nao_map)
        df['EFEITO_ADVERSO_PRESENTE_BIN'] = df['EFEITO_ADVERSO_PRESENTE_BIN'].astype('Int64')
    
    # Mapeamento para colunas de frequência de efeitos adversos específicos
    # 0 = Nunca/Não aplicável/Não presente ou não frequente
    # 1 = Presente com alguma frequência (Raramente, Ocasionalmente, Frequentemente, Sempre)
    freq_to_binary_map = {
        'nunca': 0,
        'raramente': 1,
        'ocasionalmente': 1,
        'frequentemente': 1,
        'sempre': 1
        # NA será tratado separadamente ou pelo .map resultando em NA, depois preenchido
    }

    # Colunas de frequência originais e suas novas colunas _BIN correspondentes
    efeitos_adv_especificos_map = {
        'Sobre a frequência que tem Insônia': 'EFEITO_ADVERSO_INSONIA_BIN',
        'Sobre a frequência que tem Taquicardia (coração acelerado)': 'EFEITO_ADVERSO_TAQUICARDIA_BIN',
        # 'Sobre a frequência que tem Nervosismo' - COLUNA NÃO ENCONTRADA NO CSV. Tratar como NA.
        'Sobre a frequência que tem Tremores': 'EFEITO_ADVERSO_TREMORES_BIN',
        'Sobre a frequência que tem Dor no estômago': 'EFEITO_ADVERSO_DOR_ESTOMAGO_BIN'
    }

    for col_original, col_nova_bin in efeitos_adv_especificos_map.items():
        if col_original in df.columns:
            df[col_nova_bin] = df[col_original].astype(str).str.lower().str.strip().map(freq_to_binary_map)
            
            if 'EFEITO_ADVERSO_PRESENTE_BIN' in df.columns:
                 # Se não sentiu NENHUM efeito adverso (PRESENTE_BIN == 0), então o específico também é 0.
                 df.loc[df['EFEITO_ADVERSO_PRESENTE_BIN'] == 0, col_nova_bin] = 0
                 # Se sentiu ALGUM efeito (PRESENTE_BIN == 1) mas a frequência específica não foi respondida (col_nova_bin ainda é NA), manter NA.
                 # Não preencher com 0, pois não sabemos se é ausente ou apenas não respondido.
                 # Se PRESENTE_BIN é NA, col_nova_bin também deve ser NA (o .map já pode ter feito isso se a frequência original era NA).
                 df.loc[df['EFEITO_ADVERSO_PRESENTE_BIN'].isna(), col_nova_bin] = pd.NA
            
            # Se após os condicionais acima, ainda houver NAs em col_nova_bin E PRESENTE_BIN NÃO é 0 (ou seja, é 1 ou NA),
            # isso significa que a frequência original mapeou para NA.
            # Se PRESENTE_BIN == 1, o NA em col_nova_bin deve ser mantido.
            # Se PRESENTE_BIN == NA, o NA em col_nova_bin deve ser mantido.
            # Se PRESENTE_BIN == 0, já foi tratado (col_nova_bin é 0).
            # A única situação onde NAs restantes (após .map) deveriam virar 0 é se PRESENTE_BIN == 0, o que já está coberto.
            # Ou se a política for "NA na frequência específica, quando PRESENTE_BIN é 1, significa que o efeito específico não ocorreu", então seria 0.
            # Por ora, vamos ser conservadores: NA na frequência específica quando PRESENTE_BIN=1 -> NA no _BIN.
            # Se a coluna original de frequência era NA, o .map já resulta em NA.
            # Se EFEITO_ADVERSO_PRESENTE_BIN não existir, não fazemos esses ajustes condicionais.

            df[col_nova_bin] = df[col_nova_bin].astype('Int64')
        else:
            print(f"AVISO: Coluna de frequência original '{col_original}' não encontrada. '{col_nova_bin}' será preenchida com NA.")
            df[col_nova_bin] = pd.NA
            df[col_nova_bin] = df[col_nova_bin].astype('Int64')

    # Efeitos que não têm coluna de frequência específica no CSV ou não foram mapeados:
    # Nervosismo, Ansiedade, Dor de Cabeça. Manter como NA.
    efeitos_sem_fonte_direta = [
        'EFEITO_ADVERSO_NERVOSISMO_BIN', # Não havia "Sobre a frequência que tem Nervosismo"
        'EFEITO_ADVERSO_ANSIEDADE_BIN',
        'EFEITO_ADVERSO_DOR_CABECA_BIN'
    ]
    for col_sem_fonte in efeitos_sem_fonte_direta:
        if col_sem_fonte not in df.columns or df[col_sem_fonte].isnull().all(): # Somente se não existir ou for toda NA
            df[col_sem_fonte] = pd.NA
            df[col_sem_fonte] = df[col_sem_fonte].astype('Int64')
        # Se já existe e tem dados (de uma execução anterior ou CSV), esta lógica não sobrescreverá forçadamente com NA,
        # a menos que o objetivo seja explicitamente resetá-las.
        # Dado que estamos refazendo a lógica, forçar para NA se não há fonte é seguro.
        elif col_sem_fonte in df.columns and col_sem_fonte not in efeitos_adv_especificos_map.values():
             df[col_sem_fonte] = pd.NA # Reset para os que não têm fonte mapeada
             df[col_sem_fonte] = df[col_sem_fonte].astype('Int64')


    # "Para os efeitos colaterais que você sentiu ao consumir cafeína, Com que frequência eles aparecem?" -> EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD
    efeito_adverso_freq_map = {
        'raramente (menos de 1 vez por semana)': 1,
        'pouco frequente (1-2 vezes por semana)': 2,
        'frequente (3-4 vezes por semana)': 3,
        'muito frequente (5-6 vezes por semana)': 4,
        'sempre (todos os dias que consumo cafeína)': 5,
        'não se aplica / não sinto efeitos colaterais': 0,
        'não se aplica / não sinto efeitos colaterais.': 0
    }
    col_efeito_adverso_freq_raw = 'Para os efeitos colaterais que você sentiu ao consumir cafeína, Com que frequência eles aparecem?'
    
    df['EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD'] = pd.NA # Inicializar
    if col_efeito_adverso_freq_raw in df.columns:
        df['EFEITO_ADVERSO_FREQ_NORMALIZADA'] = df[col_efeito_adverso_freq_raw].astype(str).str.lower().str.strip()
        # Usar encode_column que lida com o mapeamento e conversão para Int64
        df = encode_column(df, 'EFEITO_ADVERSO_FREQ_NORMALIZADA', efeito_adverso_freq_map, 'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD')
        df.drop(columns=['EFEITO_ADVERSO_FREQ_NORMALIZADA'], inplace=True, errors='ignore')

    # Condicionar EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD com base em EFEITO_ADVERSO_PRESENTE_BIN
    if 'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD' in df.columns and 'EFEITO_ADVERSO_PRESENTE_BIN' in df.columns:
        # Se não há efeito presente (0), a frequência codificada deve ser 0
        df.loc[df['EFEITO_ADVERSO_PRESENTE_BIN'] == 0, 'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD'] = 0
        # Se a presença de efeito é indeterminada (NA), a frequência também deve ser NA
        df.loc[df['EFEITO_ADVERSO_PRESENTE_BIN'].isna(), 'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD'] = pd.NA
        # Se EFEITO_ADVERSO_PRESENTE_BIN == 1, EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD mantém o valor do mapeamento original da pergunta de frequência.
    
    # A lógica anterior que criava EFEITO_ADVERSO_PRESENTE_BIN com base em colunas _BIN específicas foi removida
    # assim como a criação das colunas _BIN específicas baseada em keywords.

    # 2.5.2. Qual foi o seu consumo diário total de cafeína estimado (mg/dia)? Usar MG_CAFEINA_DIA processado
    # Nota: pode-se adicionar SUPLEM_DOSE_CAFEINA_MG se necessário
    df['MG_CAFEINA_TOTAL_DIA'] = df['MG_CAFEINA_DIA']

    # --- Fim da Implementação Detalhada da Codificação ---

    # --- Automatic mapping for high-cardinality and free-text fields ---
    # Dynamic encoding for occupation
    if 'Ocupação profissional' in df.columns:
        df['OCUPACAO_COD'] = pd.factorize(df['Ocupação profissional'].astype(str).str.lower().str.strip())[0] + 1
        df['OCUPACAO_COD'] = df['OCUPACAO_COD'].astype('Int64')
    # Dynamic encoding for main game
    if 'Qual é o seu jogo eletrônico principal?' in df.columns:
        df['JOGO_PRINCIPAL_COD'] = pd.factorize(df['Qual é o seu jogo eletrônico principal?'].astype(str).str.lower().str.strip())[0] + 1
        df['JOGO_PRINCIPAL_COD'] = df['JOGO_PRINCIPAL_COD'].astype('Int64')
    # Dynamic encoding for chocolate portion
    col_choc = 'Especifique a porção média de chocolate no dia que consome ( ___ )'
    if col_choc in df.columns:
        df['CHOCOLATE_PORCAO_COD'] = pd.factorize(df[col_choc].astype(str).str.lower().str.strip())[0] + 1
        df['CHOCOLATE_PORCAO_COD'] = df['CHOCOLATE_PORCAO_COD'].astype('Int64')

    # --- Create dummy variables for multiple-choice questions ---
    multicols = [
        ('Em quais momentos do dia você costuma consumir café?', 'CAFE_MOMENTO'),
        ('Em quais momentos do dia você costuma consumir energético?', 'ENERGETICO_MOMENTO'),
        ('Em quais momentos do dia você consome seu chá?', 'CHA_MOMENTO'),
        ('Em quais momentos do dia você costuma consumir o seu suplemento?', 'SUPLEM_MOMENTO'),
        ('Que tipo(s) de chocolate você consome mais frequentemente?', 'CHOC_TIPO'),
        ('Qual(is) outro(s) você joga?', 'OUTROJOGO'),
    ]
    for col, prefix in multicols:
        if col in df.columns:
            df = create_dummies(df, col, prefix)

    # Debug prints antes de exportar
    print("\n--- DEBUG: Verificando colunas de Efeitos Adversos antes da exportação ---")
    cols_to_debug = [
        'EFEITO_ADVERSO_PRESENTE_BIN', 
        'EFEITO_ADVERSO_INSONIA_BIN', 
        'EFEITO_ADVERSO_NERVOSISMO_BIN',
        'EFEITO_ADVERSO_TAQUICARDIA_BIN', 
        'EFEITO_ADVERSO_TREMORES_BIN',
        'EFEITO_ADVERSO_DOR_ESTOMAGO_BIN',
        'EFEITO_ADVERSO_ANSIEDADE_BIN',
        'EFEITO_ADVERSO_DOR_CABECA_BIN',
        'EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD'
    ]
    for col_debug in cols_to_debug:
        if col_debug in df.columns:
            print(f"Coluna: {col_debug}, Existe: True, Tipo: {df[col_debug].dtype}, Nulos: {df[col_debug].isnull().sum()}")
            print(f"Valores (primeiros 5 não nulos): {df[col_debug].dropna().head().tolist()}")
        else:
            print(f"Coluna: {col_debug}, Existe: False")
    print("--- FIM DEBUG ---\n")

    # Remover colunas "Unnamed" antes de exportar
    cols_unnamed = [col for col in df.columns if 'Unnamed:' in col]
    if cols_unnamed:
        print(f"Removendo colunas 'Unnamed': {cols_unnamed}")
        df = df.drop(columns=cols_unnamed)
    
    # Export outputs
    export_processed(df, output_csv, codebook_txt)
    return df 

if __name__ == '__main__':
    pass
    input_path = 'IC_Dados_Curados - Worksheet (1).csv'
    output_csv = 'IC_Dados_Processados.csv'
    codebook_txt = 'docs/codebook.txt'
    print(f"--- INÍCIO DA EXECUÇÃO DIRETA DE data_processing.py ---")
    print(f"Lendo de: {input_path}")
    print(f"Salvando processado em: {output_csv}")
    print(f"Salvando codebook em: {codebook_txt}")
    df_processed = process_all(input_path, output_csv, codebook_txt)
    if df_processed is not None:
        print(f"Shape do DataFrame após processamento: {df_processed.shape}")
        print(f"Dados processados e codebook gerados com sucesso em execução direta.")
    else:
        print(f"Falha no processamento em execução direta.")
    print(f"--- FIM DA EXECUÇÃO DIRETA DE data_processing.py ---") 