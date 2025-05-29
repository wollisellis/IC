import pandas as pd
import numpy as np
import os
import pytest
from src.data_processing import extract_vol_ml, extract_dose_mg, generate_codebook, export_processed

# Tests for extract_vol_ml

def test_extract_vol_ml_valid():
    assert extract_vol_ml("50 ml") == 50
    assert extract_vol_ml("200ml") == 200
    assert extract_vol_ml("Volume: 300 ML") == 300


def test_extract_vol_ml_invalid():
    assert pd.isna(extract_vol_ml("no volume"))
    assert pd.isna(extract_vol_ml(None))

# Tests for extract_dose_mg

def test_extract_dose_mg_with_mg():
    assert extract_dose_mg("200 mg") == 200
    assert extract_dose_mg("400MG") == 400


def test_extract_dose_mg_number_only():
    assert extract_dose_mg("150") == 150


def test_extract_dose_mg_invalid():
    assert pd.isna(extract_dose_mg("n/a"))
    assert pd.isna(extract_dose_mg(None))

# Tests for generate_codebook

def test_generate_codebook(tmp_path):
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["x", "y", "z"]})
    codebook_file = tmp_path / "codebook.txt"
    generate_codebook(df, str(codebook_file))
    assert codebook_file.exists()
    lines = codebook_file.read_text(encoding="utf-8").splitlines()
    # Header + two columns => at least 3 lines
    assert lines[0] == 'VariableName\tType\tUniqueValues'
    assert any('"[1, 2, 3]"' in l for l in lines)
    assert any('"[\"x\", \"y\", \"z\"]"' in l for l in lines)

# Tests for export_processed

def test_export_processed(tmp_path):
    df = pd.DataFrame({"A": [1, 2], "B": ["a", "b"]})
    csv_file = tmp_path / "out.csv"
    codebook_file = tmp_path / "codebook.txt"
    export_processed(df, str(csv_file), str(codebook_file))
    assert csv_file.exists()
    assert codebook_file.exists()
    content = csv_file.read_text(encoding="utf-8").splitlines()
    assert content[0] == 'A,B'
    assert len(content) == 3

# Test for Pontuação conversion

def test_pontuacao_conversion():
    s = pd.Series(["1,5", None, "invalid", 4])
    converted = pd.to_numeric(s.astype(str).str.replace(",", ".", regex=False), errors="coerce")
    assert converted.tolist()[0] == 1.5
    assert pd.isna(converted.tolist()[1])
    assert pd.isna(converted.tolist()[2])
    assert converted.tolist()[3] == 4.0 