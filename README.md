# IC Data Processing

![CI](https://github.com/wollisellis/IC/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)

This project processes raw questionnaire data from `IC_Dados_Curados - Worksheet (1).csv` into a numerically coded format suitable for rigorous statistical analysis. The primary script, `src/data_processing.py`, handles data loading, cleaning, PII removal, date transformations, and categorical encoding according to a defined methodology.

The main outputs are:
- `IC_Dados_Processados.csv`: The processed dataset with UTF-8 encoding and comma delimiters.
- `Livro_de_Codigos.txt`: A comprehensive codebook detailing each variable's transformation and encoding scheme.

## Project Structure

```
IC/
├── src/
│   └── data_processing.py  # Main data processing script
├── tests/
│   └── test_data_processing.py # Pytest tests for data_processing.py
├── IC_Dados_Curados - Worksheet (1).csv # Raw input data
├── RelatórioFinal_Éllis.md # Project methodology and detailed codebook
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

## Setup

Install dependencies:
```
pip install -r requirements.txt
```

## Usage

```python
from src.data_processing import process_all

# Provide paths
data_path = 'IC_Dados_Curados - Worksheet (1).csv'
output_csv = 'IC_Dados_Processados.csv'
codebook = 'Livro_de_Codigos.txt'

# Run full pipeline
df = process_all(data_path, output_csv, codebook)
```

## Tests

Run pytest:
```
pytest --maxfail=1 --disable-warnings -q
```

## Documentação

Para facilitar a navegação e manter a organização do projeto, seguem os principais documentos:

### Projetos e Relatórios
- [Metodologia e Relatório Final](docs/RelatórioFinal_Éllis.md)
- [Processamento e Metodologia de Dados](docs/Processamento%20CSV%20para%20Análise%20Estatística_.md)
- [Dados Tabulados para Análise Estatística (PDF)](Dados tabulados para análise estatística_.pdf)

### Planos e Roadmaps
- [Roadmap de Publicação do Artigo](docs/ROADMAP_ARTIGO.md)
- [Plano de Análise Estatística Focada](docs/PLANO_ANALISE_EFICIENCIA.md)

### Manuscrito
- [Esqueleto do Manuscrito](docs/Publicacao_Tese.md)

### Documentação Técnica
- [Visão Geral do Projeto (README)](README.md)
- [Código de Processamento de Dados](src/data_processing.py)
