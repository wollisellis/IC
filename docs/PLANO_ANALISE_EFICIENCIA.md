# Plano de Análise Estatística Focada

**Objetivo:** Maximizar a eficiência da análise explorando relações-chave com base nos dados coletados.

## 1. Café e Performance de Jogo
Variáveis:
- MG_CAFEINA_DIA (contínua)
- HORAS_JOGO_PRINCIPAL_MEDIA_DIA (contínua)
Teste(s):
- Correlação de Pearson (ou Spearman se distribuição não normal)
- Regressão Linear Simples: HORAS_JOGO ~ MG_CAFEINA_DIA
Visualização:
- Scatter plot com linha de regressão e banda de confiança

## 2. Nível de Jogador vs. Consumo de Cafeína
Variáveis:
- NIVEL_JOGADOR_COD (ordinal)
- MG_CAFEINA_SEMANA (contínua)
Teste(s):
- ANOVA one-way para comparar médias entre níveis
- Kruskal-Wallis se violação de pressupostos
Visualização:
- Boxplots por categoria de jogador

## 3. Consumo de Energéticos e Horas de Jogo
Variáveis:
- CONSUMO_ENERGETICOS_BIN (binária)
- HORAS_JOGO_PRINCIPAL_MEDIA_DIA
Teste(s):
- t-test de Student (independentes) ou Mann-Whitney
Visualização:
- Boxplots comparativos de horas de jogo por grupo de consumo

## 4. Suplemento de Cafeína e Efeitos Adversos
Variáveis:
- SUPLEM_DOSE_CAFEINA_MG (contínua)
- EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD (ordinal)
Teste(s):
- Correlação de Spearman
Visualização:
- Scatter plot com jitter + tamanho/paleta por frequência de efeito

## 5. Demografia x Hábitos de Consumo
### 5.1 Gênero vs Consumo
- GENERO_COD vs CONSUMO_CAFE_BIN, CONSUMO_ENERGETICOS_BIN, CONSUMO_CHA_BIN
- Tabela de contingência + Teste Qui-quadrado
### 5.2 Educação vs Consumo
- NIVEL_EDUC_COD vs MG_CAFEINA_DIA, CAFE_DIAS_SEMANA_NUM
- ANOVA ou Kruskal-Wallis

## 6. Modelagem Multivariada
### 6.1 Regressão Linear Múltipla
- Resposta: HORAS_JOGO_PRINCIPAL_MEDIA_DIA
- Preditores: MG_CAFEINA_DIA, NIVEL_JOGADOR_COD, GENERO_COD, IDADE
### 6.2 Regressão Logística
- Resposta: EFEITO_ADVERSO_BIN (criar variável binária de presença de efeito)
- Preditores: MG_CAFEINA_DIA, CONSUMO_ENERGETICOS_BIN, CONSUMO_CHA_BIN

## 7. Validação de Pressupostos
- Normalidade (Shapiro-Wilk)
- Homocedasticidade (Levene)
- Multicolinearidade (VIF)

## 8. Visualizações Prioritárias
- Histogramas e boxplots para variáveis contínuas principais
- Heatmap de correlação para variáveis numéricas
- Gráficos de barras para categóricas
- Scatter plots com linhas de tendência

## 9. Síntese Inicial
- Resumo dos principais insights e padrões observados
- Hipóteses formadas para testes formais 