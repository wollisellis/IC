# Resultados Chave da Análise Exploratória de Dados (AED)

Este documento resume os principais achados numéricos da AED realizada no notebook `notebooks/analise_exploratoria.ipynb` e via script `notebooks/gerar_descritivas.py`.

## 1. Estatísticas Descritivas Gerais
- Número total de participantes (N): 181
- Porcentagem de dados ausentes por coluna (principais):
  - `IDADE`: 1.66%
  - `HORAS_JOGO_OUTROS_MEDIA_DIA`: 2.76%
  - `Qual a marca do seu suplemento com cafeína?`: 91.71%
  - `SUPLEM_DOSE_CAFEINA_MG`: 91.71%
  - `SUPLEM_DOSES_NUM`: 91.71%
  - `MG_MULHERES`: 79.56%
  - `CHA_TIPO_PRINCIPAL_COD`: 58.56%
  - (Muitas outras colunas com alta % de NaN, especialmente as condicionais e `Unnamed`)

## 2. Variáveis Demográficas
- **Idade (`IDADE`):**
  - Média: 25.70
  - Desvio Padrão: 6.64
  - Mínimo: 18.0
  - Máximo: 56.0
- **Gênero (`GENERO_COD` - Mapeamento: 1:Masc, 2:Fem, [4,3]:Outros/PÑR):**
  - Masculino (1): 136 (75.14%)
  - Feminino (2): 37 (20.44%)
  - Outro/Prefiro não responder ([4,3]): 8 (4.42%)
- **Nível de Jogador (`NIVEL_JOGADOR_COD` - Mapeamento: 1:Amador, 2:Semi-Pro, 3:Pro):**
  - Amador/Casual (1): 146 (80.66%)
  - Semi-Profissional (2): 31 (17.13%)
  - Profissional (3): 4 (2.21%)

## 3. Variáveis de Consumo de Cafeína
- **Consumo de Cafeína Total Diário (`MG_CAFEINA_DIA`):**
  - Média: 276.37 mg
  - Desvio Padrão: 218.69 mg
  - Mediana: 228.74 mg
  - Mínimo: 0.0 mg
  - Máximo: 1092.91 mg
  - Porcentagem de NaN: 0.00%
- **Consome Café (`CONSUMO_CAFE_BIN` - Mapeamento: 1:Sim, 0:Não):**
  - Sim (1): 138 (76.24%)
  - Não (0): 43 (23.76%)
- **Consome Energéticos (`CONSUMO_ENERGETICOS_BIN` - Mapeamento: 1:Sim, 0:Não):**
  - Sim (1): 102 (56.35%)
  - Não (0): 79 (43.65%)

## 4. Variáveis de Comportamento de Jogo
- **Horas de Jogo Principal por Dia (`HORAS_JOGO_PRINCIPAL_MEDIA_DIA`):**
  - Média: 2.48 horas
  - Desvio Padrão: 1.70 horas
  - Mediana: 3.00 horas
  - Mínimo: 0.5 horas
  - Máximo: 7.0 horas

(Adicionar outras seções/variáveis conforme necessário durante a AED) 