import pandas as pd
import numpy as np
import pytest
from src.data_processing import (
    load_data, filter_consent, remove_pii,
    parse_dates, clean_numeric_columns,
    encode_column, create_dummies
)

# ---- Tests for load_data ----

def test_load_data_basic(tmp_path):
    df = pd.DataFrame({'A': [1, 2]})
    file = tmp_path / 'basic.csv'
    df.to_csv(file, index=False)
    result = load_data(str(file))
    pd.testing.assert_frame_equal(result, df)


def test_load_data_empty(tmp_path):
    file = tmp_path / 'empty.csv'
    file.write_text('col1,col2\n')
    result = load_data(str(file))
    assert result.empty


def test_load_data_missing_file():
    with pytest.raises(FileNotFoundError):
        load_data('nonexistent.csv')


# ---- Tests for filter_consent ----

def test_filter_consent_mixed():
    df = pd.DataFrame({'TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO (TCLE)': ['Aceito', 'Não Aceito', None]})
    out = filter_consent(df)
    assert len(out) == 1
    assert out['TCLE_ACEITE'].iloc[0] == 1


def test_filter_consent_all_accepted():
    df = pd.DataFrame({'TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO (TCLE)': ['Aceito', 'Aceito']})
    out = filter_consent(df)
    assert len(out) == 2
    assert all(out['TCLE_ACEITE'] == 1)


def test_filter_consent_none():
    df = pd.DataFrame({'TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO (TCLE)': ['Nao', '']})
    out = filter_consent(df)
    assert out.empty


# ---- Tests for remove_pii ----

def test_remove_pii_present():
    df = pd.DataFrame({'E-mail (para o envio do TCLE)': ['x'], 'Como você prefere ser chamado(a/e)?': ['y'], 'ID': [1]})
    out = remove_pii(df)
    assert 'E-mail (para o envio do TCLE)' not in out.columns
    assert 'Como você prefere ser chamado(a/e)?' not in out.columns
    assert 'ID' in out.columns


def test_remove_pii_missing():
    df = pd.DataFrame({'ID': [1], 'Name': ['A']})
    out = remove_pii(df)
    assert set(out.columns) == {'ID', 'Name'}


def test_remove_pii_empty_df():
    df = pd.DataFrame()
    out = remove_pii(df)
    assert out.empty


# ---- Tests for parse_dates ----

def test_parse_dates_basic():
    df = pd.DataFrame({'Data': ['2023-01-01 00:00:00', '2023-12-31 23:59:59'],
                       'Data de Nascimento': ['01/01/2000', '31/12/1990']})
    out = parse_dates(df)
    assert 'TIMESTAMP_RESPOSTA' in out.columns
    assert 'IDADE' in out.columns
    assert isinstance(out['IDADE'].dtype, pd.Int64Dtype)


def test_parse_dates_invalid_birth():
    df = pd.DataFrame({'Data': ['2023-01-01 00:00:00'], 'Data de Nascimento': ['invalid']})
    out = parse_dates(df)
    assert pd.isna(out['IDADE'].iloc[0])


def test_parse_dates_empty_fields():
    df = pd.DataFrame({'Data': [None], 'Data de Nascimento': [None]})
    out = parse_dates(df)
    assert pd.isna(out['TIMESTAMP_RESPOSTA'].iloc[0])
    assert pd.isna(out['IDADE'].iloc[0])


# ---- Tests for clean_numeric_columns ----

def test_clean_numeric_replace_comma():
    df = pd.DataFrame({'col': ['1,5', '2,0']})
    out = clean_numeric_columns(df, {'col': 'new'})
    assert out['new'].tolist() == [1.5, 2.0]


def test_clean_numeric_error_to_nan():
    df = pd.DataFrame({'col': ['#ERROR!', '']})
    out = clean_numeric_columns(df, {'col': 'new'})
    assert pd.isna(out['new'].iloc[0])
    assert pd.isna(out['new'].iloc[1])


def test_clean_numeric_mixed():
    df = pd.DataFrame({'c1': ['10', '5,5', 'abc'], 'c2': ['1,0', '#ERROR!', '3']})
    out = clean_numeric_columns(df, {'c1': 'n1', 'c2': 'n2'})
    assert out['n1'].iloc[0] == 10.0
    assert out['n1'].iloc[1] == 5.5
    assert pd.isna(out['n1'].iloc[2])
    assert out['n2'].iloc[0] == 1.0
    assert pd.isna(out['n2'].iloc[1])
    assert out['n2'].iloc[2] == 3.0


# ---- Tests for encode_column ----

def test_encode_column_basic():
    df = pd.DataFrame({'col': ['A', 'B', 'C']})
    mapping = {'A': 1, 'B': 2}
    out = encode_column(df, 'col', mapping, 'new')
    assert out['new'].tolist() == [1, 2, pytest.raises(ValueError) if False else pd.NA]


def test_encode_column_strip():
    df = pd.DataFrame({'col': [' A ', 'B']})
    mapping = {'A': 1, 'B': 2}
    out = encode_column(df, 'col', mapping, 'new')
    assert out['new'].tolist() == [1, 2]


def test_encode_column_unknown():
    df = pd.DataFrame({'col': ['X']})
    mapping = {'A': 1}
    out = encode_column(df, 'col', mapping, 'new')
    assert pd.isna(out['new'].iloc[0])


# ---- Tests for create_dummies ----

def test_create_dummies_single():
    df = pd.DataFrame({'col': ['a, b', None]})
    out = create_dummies(df, 'col', 'PRE')
    # should create PRE_A and PRE_B
    assert 'PRE_A' in out.columns and 'PRE_B' in out.columns
    # first row a->1, b->1; second row -> NaN
    assert out.loc[0, 'PRE_A'] == 1 and out.loc[0, 'PRE_B'] == 1
    assert pd.isna(out.loc[1, 'PRE_A'])


def test_create_dummies_multiple():
    df = pd.DataFrame({'col': ['x, y, z']})
    out = create_dummies(df, 'col', 'D')
    for cat in ['X', 'Y', 'Z']:
        assert out[f'D_{cat}'].iloc[0] == 1


def test_create_dummies_empty():
    df = pd.DataFrame({'col': [pd.NA]})
    out = create_dummies(df, 'col', 'P')
    # No dummy columns should be created
    assert all(not c.startswith('P_') for c in out.columns) 