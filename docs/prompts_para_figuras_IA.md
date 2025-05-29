# Guia de Prompts para Geração de Figuras por IA

Este documento fornece prompts sugeridos para gerar as figuras do estudo "Padrões de Consumo de Cafeína em Jogadores de Esports: Um Estudo Transversal" utilizando uma ferramenta de Inteligência Artificial capaz de processar dados e criar visualizações estatísticas.

**Nota Importante sobre Nomes de Variáveis:**
*   Nos prompts abaixo, quando a instrução se refere a uma **"coluna"** do arquivo de dados (ex: "Use a coluna 'MG_CAFEINA_TOTAL_DIA'"), o nome técnico da variável, conforme consta no arquivo `IC_Dados_Processados.csv`, **deve ser usado**. Isso é essencial para que a IA possa localizar e processar os dados corretamente.
*   Para entender a correspondência entre os nomes técnicos no dataset e os nomes descritivos usados no manuscrito (e nos títulos/rótulos dos gráficos aqui sugeridos), consulte o arquivo `docs/variaveis_map.md`.
*   Os títulos dos gráficos, rótulos dos eixos e descrições de categorias nos prompts já utilizam linguagem natural e os nomes descritivos esperados para a visualização final.

**Pré-requisitos para a IA:**
*   Acesso ao arquivo de dados `IC_Dados_Processados.csv` (localizado na raiz do projeto).
*   Capacidade de ler arquivos CSV (e interpretá-los como um pandas DataFrame ou estrutura similar).
*   Capacidade de gerar gráficos estatísticos (histogramas, boxplots, scatter plots).
*   Capacidade de filtrar e agrupar dados conforme as especificações.

---

## Figura 1: Distribuição do Consumo Diário de Cafeína

**Descrição conforme `Publicacao_Tese.md`:** Histograma ou boxplot mostrando a distribuição da variável Consumo Diário Total de Cafeína (mg) para a amostra total, evidenciando a assimetria e outliers.

**Contexto dos Dados para a Figura 1:**
*   Arquivo de dados a ser usado: `IC_Dados_Processados.csv`.
*   Coluna principal: `MG_CAFEINA_TOTAL_DIA`. Esta coluna contém valores numéricos que representam o consumo total diário de cafeína em miligramas para cada participante.

**Sugestão de Prompt para IA (Opção 1: Histograma):**
```
Analise o arquivo 'IC_Dados_Processados.csv'.
Focando na coluna 'MG_CAFEINA_TOTAL_DIA' (valores numéricos do consumo diário de cafeína em mg),
Gere um histograma para esta coluna.
Título do gráfico: 'Figura 1: Distribuição do Consumo Diário de Cafeína'
Rótulo do eixo X: 'Consumo Diário Total de Cafeína (mg)'
Rótulo do eixo Y: 'Frequência (Número de Participantes)'
Use um número de bins que ilustre adequadamente a forma da distribuição, sua assimetria e a presença de outliers.
```

**Sugestão de Prompt para IA (Opção 2: Boxplot):**
```
Analise o arquivo 'IC_Dados_Processados.csv'.
Focando na coluna 'MG_CAFEINA_TOTAL_DIA' (valores numéricos do consumo diário de cafeína em mg),
Gere um boxplot vertical para esta coluna.
Título do gráfico: 'Figura 1: Distribuição do Consumo Diário de Cafeína'
Rótulo do eixo Y: 'Consumo Diário Total de Cafeína (mg)'
O boxplot deve cobrir a amostra total, então o eixo X não necessita de rótulos de categoria.
Certifique-se de que os outliers sejam claramente exibidos.
```

---

## Figura 2: Consumo Diário de Cafeína por Nível de Experiência do Jogador

**Descrição conforme `Publicacao_Tese.md`:** Boxplots comparando o Consumo Diário Total de Cafeína (mg) entre os grupos Amador/Casual e Semi-Profissional (Nível de Experiência do Jogador).

**Contexto dos Dados para a Figura 2:**
*   Arquivo de dados a ser usado: `IC_Dados_Processados.csv`.
*   Coluna de valor: `MG_CAFEINA_TOTAL_DIA` (valores numéricos do consumo diário de cafeína em mg).
*   Coluna de agrupamento: `NIVEL_JOGADOR_COD`. Esta coluna contém códigos numéricos: 1 para 'Amador/Casual', 2 para 'Semi-Profissional', e 3 para 'Profissional'. Para esta figura, focaremos apenas nos códigos 1 e 2.

**Sugestão de Prompt para IA:**
```
Analise o arquivo 'IC_Dados_Processados.csv'.
Primeiro, filtre os dados para incluir apenas participantes onde a coluna 'NIVEL_JOGADOR_COD' é igual a 1 (representando 'Amador/Casual') ou igual a 2 (representando 'Semi-Profissional').
Para estes dois grupos filtrados, gere boxplots comparativos mostrando a distribuição da coluna 'MG_CAFEINA_TOTAL_DIA' (consumo diário de cafeína em mg).
Título do gráfico: 'Figura 2: Consumo Diário de Cafeína por Nível de Experiência do Jogador'
Rótulo do eixo X: 'Nível de Experiência do Jogador', com as categorias claramente identificadas como 'Amador/Casual' e 'Semi-Profissional'.
Rótulo do eixo Y: 'Consumo Diário Total de Cafeína (mg)'
Certifique-se de que os outliers sejam exibidos em cada boxplot.
```

---

## Figura 3: Diagrama de Dispersão - Consumo de Cafeína vs. Horas de Jogo

**Descrição conforme `Publicacao_Tese.md`:** Scatter plot mostrando a relação entre o Consumo Diário Total de Cafeína (mg) e as Horas Médias de Jogo Principal por Dia.

**Contexto dos Dados para a Figura 3:**
*   Arquivo de dados a ser usado: `IC_Dados_Processados.csv`.
*   Coluna para o eixo X: `HORAS_JOGO_PRINCIPAL_MEDIA_DIA`. Esta coluna contém valores numéricos representando as horas médias que os participantes dedicam ao seu jogo principal por dia.
*   Coluna para o eixo Y: `MG_CAFEINA_TOTAL_DIA`. Esta coluna contém valores numéricos do consumo total diário de cafeína em miligramas.
*   Tratamento de Ausentes: Linhas com valores ausentes (NaN) em qualquer uma dessas duas colunas devem ser excluídas antes da plotagem.

**Sugestão de Prompt para IA:**
```
Analise o arquivo 'IC_Dados_Processados.csv'.
Considere as colunas 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' (horas de jogo) e 'MG_CAFEINA_TOTAL_DIA' (consumo de cafeína em mg).
Antes de plotar, remova quaisquer participantes (linhas) que tenham valores ausentes (NaN) em 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA' ou em 'MG_CAFEINA_TOTAL_DIA'.
Gere um diagrama de dispersão (scatter plot) para visualizar a relação entre estas duas variáveis.
Eixo X: deve representar os valores da coluna 'HORAS_JOGO_PRINCIPAL_MEDIA_DIA'.
Eixo Y: deve representar os valores da coluna 'MG_CAFEINA_TOTAL_DIA'.
Título do gráfico: 'Figura 3: Consumo de Cafeína vs. Horas de Jogo'
Rótulo do eixo X: 'Horas Médias de Jogo Principal por Dia'
Rótulo do eixo Y: 'Consumo Diário Total de Cafeína (mg)'
```

---

**Nota Importante sobre Ferramentas de IA:**
A eficácia destes prompts dependerá significativamente das capacidades da IA específica que você utilizar. IAs geradoras de imagens de propósito geral (como DALL-E, Midjourney) provavelmente **não** conseguirão interpretar estes prompts para gerar gráficos estatisticamente precisos a partir dos seus dados. Estes prompts são mais adequados para IAs com funcionalidades de análise de dados e visualização incorporadas, ou como um guia detalhado para você recriar os gráficos em ferramentas como Python (com Matplotlib/Seaborn), R (com ggplot2), ou Excel, se necessário.

Para garantir a precisão científica, a consistência com os resultados do estudo e a possibilidade de ajustes finos (como fontes, cores, tamanhos específicos para publicação), a melhor abordagem continua sendo a geração dos gráficos via código (como o utilizado em `notebooks/gerar_descritivas.py`). Esse código pode ser ajustado para atender a requisitos de estilo específicos de periódicos ou da sua instituição. 