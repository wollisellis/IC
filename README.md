# Análise do Consumo de Cafeína em Jogadores de E-Sports Brasileiros e Artigo Associado

Este repositório contém os dados, scripts de processamento e o manuscrito resultante de um estudo transversal sobre os padrões de consumo de cafeína, motivações e efeitos adversos associados em jogadores de e-sports brasileiros.

## Visão Geral do Projeto

O objetivo principal desta pesquisa foi caracterizar os padrões de consumo de cafeína em jogadores de e-sports no Brasil e investigar associações com variáveis demográficas, nível de experiência e indicadores de bem-estar. Os resultados e discussões detalhadas estão compilados no manuscrito `docs/JISSN_Submission_Draft.md`.

## Estrutura de Diretórios Principais

```
IC/
├── .github/             # Configurações de CI/CD (ex: GitHub Actions)
├── docs/                # Documentação e manuscrito
│   ├── JISSN_Submission_Draft.md  # Manuscrito principal do estudo
│   └── references.bib     # Referências bibliográficas
├── notebooks/           # Jupyter notebooks para análises exploratórias e testes
│   ├── outputs/           # Saídas geradas pelos notebooks (figuras, relatórios parciais)
│   └── archived_notebooks/ # Notebooks de exploração e desenvolvimento inicial
├── src/                 # Código fonte para processamento e análise de dados
│   └── data_processing.py # Script principal para limpeza, tratamento e cálculo de variáveis
├── tests/               # Testes automatizados para o código em src/
├── data/                # (SUGESTÃO) Idealmente, dados brutos e processados estariam aqui
│                        # Atualmente, os arquivos de dados estão na raiz:
├── IC_Dados_Curados_Cafeina_Recalculada_v3.csv # Dados curados com cafeína recalculada
├── IC_Dados_Processados.csv # Dados processados utilizados nas análises finais
├── requirements.txt     # Dependências do projeto Python
├── run_pipeline.py      # Script para orquestrar o pipeline de processamento de dados
├── pipeline.log         # Log da execução do pipeline
└── README.md            # Este arquivo
```

## Pré-requisitos

- Python 3.8 ou superior
- Ambiente virtual (recomendado: venv ou virtualenv)

## Instalação e Configuração

1.  Clone o repositório:
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd IC
    ```

2.  Crie e ative um ambiente virtual:
    ```bash
    # No Windows PowerShell
    python -m venv venv
    venv\Scripts\activate

    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Instale as dependências:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

## Como Usar

### 1. Processamento de Dados
Para executar o pipeline completo de processamento de dados, que inclui limpeza, tratamento dos dados do questionário e cálculo da cafeína consumida:
```bash
python run_pipeline.py
```
Verifique o arquivo `pipeline.log` para acompanhar a execução. Os dados processados são salvos (e.g., `IC_Dados_Processados.csv`).

### 2. Análise dos Resultados e Manuscrito
Os principais resultados, análises estatísticas e discussões estão detalhados no manuscrito:
`docs/JISSN_Submission_Draft.md`

As análises exploratórias e alguns testes estatísticos podem ser encontrados nos notebooks dentro de `notebooks/`.

## Dados Principais

-   `IC_Dados_Curados_Cafeina_Recalculada_v3.csv`: Contém os dados brutos do questionário após uma etapa inicial de curadoria e o recálculo detalhado do consumo de cafeína.
-   `IC_Dados_Processados.csv`: Dataset final utilizado para as análises estatísticas apresentadas no manuscrito.
-   `Livro_de_Codigos.txt`: Descreve as variáveis presentes nos datasets.

## Testes Automatizados

Para garantir a qualidade e a corretude do código de processamento em `src/`:
```bash
pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80
```
Certifique-se de que todos os testes passam antes de realizar novas análises.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues para reportar bugs ou sugerir melhorias, ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE.md) (Sugestão: Adicione um arquivo LICENSE.md com o texto da licença MIT ou outra de sua escolha).
