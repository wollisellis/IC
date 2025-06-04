# Projeto IC - Análises Estatísticas de Consumo de Cafeína em E-Sports

Este repositório contém scripts em Python para:

- Calcular estatísticas descritivas e gerar visualizações.
- Executar análises estatísticas inferenciais (testes de hipóteses e regressões).
- Gerar relatórios em arquivos Markdown e TXT para inclusão na tese.

## Estrutura de Diretórios
```
IC/
├── notebooks/
│   ├── analise_estatistica_inferencial.py   # Análises inferenciais e geração de resultados
│   ├── gerar_descritivas.py                 # Estatísticas descritivas e geração de figuras
│   ├── test_analises.py                     # Testes com pytest para funções de análise
│   ├── outputs/                             # Diretório de saída (figuras e relatórios)
│   └── archived_notebooks/                  # Notebooks exploratórios arquivados
├── requirements.txt                         # Dependências do projeto
└── README.md                                # Documentação de uso
```

## Pré-requisitos

- Python 3.8 ou superior
- Ambiente virtual (recomendado: venv ou virtualenv)

## Instalação
```bash
# No Windows PowerShell
python -m venv venv
venv\Scripts\activate

# No macOS/Linux
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

## Execução dos Scripts

### 1. Estatísticas Descritivas
```bash
python notebooks/gerar_descritivas.py
```
- Gera `notebooks/outputs/estatisticas_descritivas.md` com tabelas em Markdown.
- Salva figuras em `notebooks/outputs/` (ex.: `figura1_distribuicao_cafeina.png`).

### 2. Análises Inferenciais
```bash
python notebooks/analise_estatistica_inferencial.py
```
- Gera `notebooks/outputs/resultados_inferenciais.txt` com resultados dos testes.
- Salva figuras em `notebooks/outputs/` (ex.: `figura3_cafeina_vs_horas_jogo.png`).

## Testes Automatizados
Para garantir a qualidade do código e as transformações de dados:
```bash
pytest --cov=notebooks --cov-report=term-missing --cov-fail-under=80
```

## Observações

- Atualize `requirements.txt` com versões específicas após instalar dependências:
  ```bash
  pip freeze > requirements.txt
  ```
- Notebooks exploratórios estão arquivados em `notebooks/archived_notebooks/` e não fazem parte do pipeline de produção.

## Contribuição
Contribuições são bem-vindas! Abra issues ou pull requests para melhorias.

## Licença
Este projeto está licenciado sob [INSERIR LICENÇA AQUI].
