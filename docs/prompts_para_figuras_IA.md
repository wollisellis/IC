# Guia de Prompts para Geração de Figuras por IA

Este documento fornece prompts sugeridos para gerar as figuras do estudo "Padrões de Consumo de Cafeína em Jogadores de Esports: Um Estudo Transversal" utilizando uma ferramenta de Inteligência Artificial capaz de processar dados e criar visualizações estatísticas.

**Pré-requisitos para a IA:**
*   Acesso ao arquivo de dados `IC_Dados_Processados.csv` (localizado na raiz do projeto).
*   Capacidade de ler arquivos CSV (e interpretá-los como um pandas DataFrame ou estrutura similar).
*   Capacidade de gerar gráficos estatísticos (histogramas, boxplots, scatter plots).
*   Capacidade de filtrar e agrupar dados conforme as especificações.

---

## Figura 1: Distribuição do Consumo Diário de Cafeína (MG_CAFEINA_TOTAL_DIA)

**Descrição conforme `Publicacao_Tese.md`:** Histograma ou boxplot mostrando a distribuição da variável `MG_CAFEINA_TOTAL_DIA` para a amostra total, evidenciando a assimetria e outliers.

**Sugestão de Prompt para IA (Opção 1: Histograma):**
```
Analise o arquivo 'IC_Dados_Processados.csv'.
Gere um histograma para a coluna 'MG_CAFEINA_TOTAL_DIA'.
Título do gráfico: 'Figura 1: Distribuição do Consumo Diário de Cafeína'
Rótulo do eixo X: 'Consumo Diário Total de Cafeína (mg)'
Rótulo do eixo Y: 'Frequência'
Use um número de bins adequado para mostrar claramente a forma da distribuição, a assimetria e os outliers.
```

**Sugestão de Prompt para IA (Opção 2: Boxplot):**
```
Analise o arquivo 'IC_Dados_Processados.csv'.
Gere um boxplot vertical para a coluna 'MG_CAFEINA_TOTAL_DIA'.
Título do gráfico: 'Figura 1: Distribuição do Consumo Diário de Cafeína'
Rótulo do eixo Y: 'Consumo Diário Total de Cafeína (mg)'
Remova o rótulo do eixo X ou deixe-o em branco, pois é para a amostra total.
Certifique-se de que os outliers sejam exibidos.
```

---

## Figura 2: Consumo Diário de Cafeína (MG_CAFEINA_TOTAL_DIA) por Nível de Jogador

**Descrição conforme `Publicacao_Tese.md`:** Boxplots comparando `MG_CAFEINA_TOTAL_DIA` entre os grupos Amador/Casual e Semi-Profissional.

**Sugestão de Prompt para IA:**
```
Analise o arquivo 'IC_Dados_Processados.csv'.
Filtre os dados para incluir apenas onde 'NIVEL_JOGADOR_COD' é 1 (Amador/Casual) ou 2 (Semi-Profissional).
Gere boxplots comparativos da coluna 'MG_CAFEINA_TOTAL_DIA' para estes dois grupos.
Título do gráfico: 'Figura 2: Consumo Diário de Cafeína por Nível de Jogador'
Rótulo do eixo X: 'Nível do Jogador' (com categorias 'Amador/Casual' e 'Semi-Profissional')
Rótulo do eixo Y: 'Consumo Diário Total de Cafeína (mg)'
Exiba os outliers em cada boxplot.
```

---

## Figura 3: Diagrama de Dispersão - Consumo de Cafeína vs. Horas de Jogo

**Descrição conforme `Publicacao_Tese.md`:** Scatter plot mostrando a relação entre `MG_CAFEINA_TOTAL_DIA` e `HORAS_JOGO_PRINCIPAL_MEDIA_DIA`.

**Sugestão de Prompt para IA:**
```
Analise o arquivo 'IC_Dados_Processados.csv'.
Gere um diagrama de dispersão (scatter plot).
Eixo X: coluna 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA'
Eixo Y: coluna 'MG_CAFEINA_TOTAL_DIA'
Título do gráfico: 'Figura 3: Consumo de Cafeína vs. Horas de Jogo'
Rótulo do eixo X: 'Horas Médias de Jogo Principal por Dia'
Rótulo do eixo Y: 'Consumo Diário Total de Cafeína (mg)'
Remova quaisquer linhas com valores NaN em 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' ou 'MG_CAFEINA_TOTAL_DIA' antes de plotar.
```

---

**Nota Importante:**
A eficácia destes prompts dependerá significativamente das capacidades da IA específica que você utilizar. IAs geradoras de imagens de propósito geral (como DALL-E, Midjourney) provavelmente **não** conseguirão interpretar estes prompts para gerar gráficos estatisticamente precisos a partir dos seus dados. Estes prompts são mais adequados para IAs com funcionalidades de análise de dados e visualização incorporadas, ou como um guia detalhado para você recriar os gráficos em ferramentas como Python (com Matplotlib/Seaborn), R (com ggplot2), ou Excel, se necessário.

Para garantir a precisão científica, a consistência com os resultados do estudo e a possibilidade de ajustes finos (como fontes, cores, tamanhos específicos para publicação), a melhor abordagem continua sendo a geração dos gráficos via código (como o utilizado em `notebooks/gerar_descritivas.py`). Esse código pode ser ajustado para atender a requisitos de estilo específicos de periódicos ou da sua instituição. 