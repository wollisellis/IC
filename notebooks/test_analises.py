import pytest
import pandas as pd
import os
from notebooks.analise_estatistica_inferencial import carregar_dados

# Criar um diretório temporário para arquivos de teste CSV
@pytest.fixture(scope="module")
def temp_csv_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("data")

# Fixture para criar um arquivo CSV de teste válido
@pytest.fixture
def valid_csv_file(temp_csv_dir):
    content = "IDADE,GENERO_COD,NIVEL_JOGADOR_COD,MG_CAFEINA_DIA\n25,1,1,100\n30,2,2,150.5\n22,1,1,NA"
    file_path = temp_csv_dir.join("valid_data.csv")
    with open(file_path, 'w') as f:
        f.write(content)
    return str(file_path)

# Fixture para criar um arquivo CSV de teste com cabeçalho mas sem dados
@pytest.fixture
def empty_data_csv_file(temp_csv_dir):
    content = "IDADE,GENERO_COD,NIVEL_JOGADOR_COD,MG_CAFEINA_DIA\n"
    file_path = temp_csv_dir.join("empty_data.csv")
    with open(file_path, 'w') as f:
        f.write(content)
    return str(file_path)

# Fixture para criar um arquivo CSV de teste com colunas faltantes
@pytest.fixture
def missing_cols_csv_file(temp_csv_dir):
    content = "IDADE,GENERO_COD\n35,1\n40,2"
    file_path = temp_csv_dir.join("missing_cols.csv")
    with open(file_path, 'w') as f:
        f.write(content)
    return str(file_path)
    
# Teste com arquivo CSV válido
def test_carregar_dados_valid_file(valid_csv_file):
    df = carregar_dados(valid_csv_file)
    assert isinstance(df, pd.DataFrame), "Should return a DataFrame"
    assert not df.empty, "DataFrame should not be empty"
    assert df.shape == (3, 4), "DataFrame shape should be (3, 4)"
    assert df['MG_CAFEINA_DIA'].isnull().sum() == 1, "MG_CAFEINA_DIA should have one NaN after coerce"
    assert pd.api.types.is_numeric_dtype(df['IDADE']), "IDADE should be numeric"
    assert pd.api.types.is_integer_dtype(df['GENERO_COD']), "GENERO_COD should be Int64" #_COD são convertidas para Int64

# Teste com arquivo CSV que tem apenas cabeçalho
def test_carregar_dados_empty_data_file(empty_data_csv_file):
    df = carregar_dados(empty_data_csv_file)
    assert isinstance(df, pd.DataFrame), "Should return a DataFrame for empty data file"
    assert df.empty, "DataFrame should be empty if CSV has only headers"

# Teste com arquivo inexistente
def test_carregar_dados_non_existent_file():
    df = carregar_dados("non_existent_file.csv")
    assert isinstance(df, pd.DataFrame), "Should return an empty DataFrame for non-existent file"
    assert df.empty, "DataFrame should be empty for non-existent file"

# Teste com arquivo que possui colunas numéricas e categóricas chave faltando
def test_carregar_dados_missing_key_cols(missing_cols_csv_file, capsys):
    df = carregar_dados(missing_cols_csv_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2) # Carrega o que existe
    
    captured = capsys.readouterr()
    # Verifica se os avisos sobre colunas faltantes foram impressos (exemplos)
    assert "AVISO: Coluna numérica chave MG_CAFEINA_DIA não encontrada." in captured.out
    assert "AVISO: Coluna chave NIVEL_JOGADOR_COD não encontrada no DataFrame." in captured.out
    # Adicione mais asserts para outras colunas chave que deveriam estar ausentes

# Teste para verificar a conversão de tipos (numérico e Int64 para categóricas)
def test_carregar_dados_type_conversion(temp_csv_dir):
    # Test data with mixed types for a category that should be Int64
    # And a numeric column that should be float after coercion
    content = "NIVEL_JOGADOR_COD,MG_CAFEINA_DIA,GENERO_COD,IDADE\n1,100,1.0,25\n2.0,bla,0,30\n1,50.0,1,string_idade"
    file_path = temp_csv_dir.join("type_conversion_test.csv")
    with open(file_path, 'w') as f:
        f.write(content)
    
    df = carregar_dados(str(file_path))
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 3 # 3 linhas
    
    # NIVEL_JOGADOR_COD e GENERO_COD deveriam ser Int64 após conversão
    assert pd.api.types.is_integer_dtype(df['NIVEL_JOGADOR_COD']), "NIVEL_JOGADOR_COD should be Int64"
    assert df['NIVEL_JOGADOR_COD'].tolist() == [1, 2, 1], "NIVEL_JOGADOR_COD values incorrect"
    
    assert pd.api.types.is_integer_dtype(df['GENERO_COD']), "GENERO_COD should be Int64"
    assert df['GENERO_COD'].tolist() == [1, 0, 1], "GENERO_COD values incorrect"

    # MG_CAFEINA_DIA deveria ser float, com 'bla' coercido para NaN
    assert pd.api.types.is_numeric_dtype(df['MG_CAFEINA_DIA'])
    assert not pd.api.types.is_integer_dtype(df['MG_CAFEINA_DIA']) # Deve ser float
    assert df['MG_CAFEINA_DIA'].isnull().sum() == 1, "MG_CAFEINA_DIA should have one NaN from 'bla'"
    
    # IDADE deveria ser float (ou object se não puder converter tudo), com 'string_idade' coercido para NaN
    assert pd.api.types.is_numeric_dtype(df['IDADE'])
    assert df['IDADE'].isnull().sum() == 1, "IDADE should have one NaN from 'string_idade'" 