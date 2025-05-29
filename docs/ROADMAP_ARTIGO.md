# Roadmap para Publicação de Artigo Científico

**Título Provisório do Artigo:** (Ex: "Perfil de Consumo de Cafeína e Hábitos de Jogo em Jogadores Brasileiros de E-sports: Uma Análise Quantitativa")

**Autores:** Éllis Wollis Malta Abhulime [Seu Nome Aqui], [Profa. Dra. Fabiana Braga Benatti

**Periódicos Alvo (Sugestões Iniciais - a serem refinadas após análise):**
*   Revista Brasileira de Medicina do Esporte
*   Journal of the International Society of Sports Nutrition
*   Computers in Human Behavior
*   Cyberpsychology, Behavior, and Social Networking
*   International Journal of Esports

**Fases do Projeto:**

**Fase 1: Finalização do Processamento de Dados e Análise Exploratória (AED)**

1.1. **Implementação Completa da Codificação de Dados (em `src/data_processing.py`):**
    *   [ ] Detalhar e implementar a codificação para **TODAS** as variáveis categóricas e textuais restantes, conforme a metodologia descrita em `RelatórioFinal_Éllis.md`. Isso inclui:
        *   [x] `NIVEL_EDUC_COD`
        *   [x] `NIVEL_JOGADOR_COD`
        *   [x] `CONSUMO_CAFE_BIN`
        *   [x] `CAFE_DIAS_SEMANA_NUM`
        *   [x] `CAFE_RECIPIENTE_VOL_ML` (extração numérica) e `CAFE_RECIPIENTE_TIPO_COD`
        *   [x] `CAFE_VEZES_DIA_NUM` (extração numérica)
        *   [x] `CAFE_TIPO_PRINCIPAL_COD`
        *   [x] `HORAS_JOGO_PRINCIPAL_MEDIA_DIA` e `HORAS_JOGO_OUTROS_MEDIA_DIA` (codificação híbrida)
        *   [x] `SUPLEM_DOSE_CAFEINA_MG` (extração numérica) e `SUPLEM_DOSES_NUM`
        *   [x] `ESTADO_RESIDENCIA_COD`
        *   [x] `CIDADE_RESIDENCIA_PREENCHIDO`
        *   [x] `OCUPACAO_COD` (alta cardinalidade, usar mapeamento de `RelatórioFinal_Éllis.md`)
        *   [x] `COMPETIU_CAMPEONATOS_BIN`
        *   [x] `PLATAFORMA_PRINCIPAL_COD`
        *   [x] `JOGO_PRINCIPAL_COD` (alta cardinalidade, usar mapeamento de `RelatórioFinal_Éllis.md`)
        *   [x] `TEMPO_JOGO_PRINCIPAL_COD`
        *   [x] `PARTE_TIME_ORG_BIN` e `NOME_TIME_ORG_PREENCHIDO_BIN`
        *   [x] `CAFE_CONSUMO_OUTRO_TIPO_COD`
        *   [x] `CONSUMO_ENERGETICOS_BIN`
        *   [x] `ENERGETICO_DIAS_SEMANA_NUM`
        *   [x] `ENERGETICO_TIPO_PRINCIPAL_COD`
        *   [x] `ENERGETICO_TAMANHO_RECIPIENTE_COD` e `ENERGETICO_TAMANHO_RECIPIENTE_ML_NUM`
        *   [x] `ENERGETICO_VEZES_DIA_NUM`
        *   [x] `CONSUMO_CHA_BIN`
        *   [x] `CHA_DIAS_SEMANA_NUM`
        *   [x] `CHA_TIPO_PRINCIPAL_COD`
        *   [x] `CHA_RECIPIENTE_COD` e `CHA_RECIPIENTE_VOL_ML_NUM`
        *   [x] `CHA_VEZES_DIA_NUM`
        *   [~] `CHOCOLATE_PORCAO_COD` (estrutura implementada, mapeamento de texto livre pendente de revisão pelo usuário)
        *   [~] `EFEITO_ADVERSO_FREQUENCIA_DESCRITA_COD` (estrutura implementada, mapeamento de texto livre pendente de revisão pelo usuário)
        *   [ ] E todas as outras variáveis mencionadas na Seção 2.5 de `RelatórioFinal_Éllis.md`.
    *   [ ] Implementar a criação de **TODAS** as variáveis dummy para questões de múltipla escolha, conforme Seção 2.5.3 (ex: `CAFE_MOMENTO_*`, `CHOC_TIPO_*`, `OUTROJOGO_*`, etc.).
        *   Revisar a função `create_dummies` para garantir robustez e correta nomeação das colunas dummy.
    *   **Entregável Chave:** Script `src/data_processing.py` totalmente implementado e testado.

1.2. **Geração do Livro de Códigos Detalhado (`Livro_de_Codigos.txt`):**
    *   [ ] Aprimorar significativamente a função `export_processed` (ou criar uma nova `generate_codebook(df, codebook_path, methodology_path)`) para gerar `Livro_de_Codigos.txt` no formato exato especificado na Seção 3.2 e exemplificado na Seção 4.0 do `RelatórioFinal_Éllis.md`.
        *   O livro de códigos deve incluir para cada variável: `ID_ORIGINAL_QUESTAO`, `NOME_COLUNA_ORIGINAL`, `NOME_VARIAVEL_PROCESSADA(S)`, `DESCRICAO_VARIAVEL`, `TIPO_VARIAVEL_ORIGINAL`, `TIPO_VARIAVEL_PROCESSADA`, `ESQUEMA_CODIFICACAO_TRANSFORMACAO`, `VALORES_UNICOS_ORIGINAIS_E_CODIGOS_MAPEADOS`, e `NOTAS_CODIFICACAO`.
        *   Considerar extrair informações do `RelatórioFinal_Éllis.md` para popular partes do livro de códigos programaticamente, se viável, ou preparar um template.
    *   **Entregável Chave:** `Livro_de_Codigos.txt` completo, preciso e formatado conforme a metodologia.

1.3. **Execução do Pipeline e Geração dos Dados Finais:**
    *   [ ] Executar o `src/data_processing.py` completo sobre `IC_Dados_Curados - Worksheet (1).csv`.
    *   **Entregável Chave:** Arquivo `IC_Dados_Processados.csv` final.

1.4. **Validação Rigorosa dos Dados Processados:**
    *   [ ] Revisão manual de uma amostra de `IC_Dados_Processados.csv` contra o `Livro_de_Codigos.txt` e o arquivo original para garantir a precisão da codificação.
    *   [ ] Análise da distribuição de valores ausentes (NaN) por variável no dataset processado. Justificar/documentar a natureza dos NaNs.
    *   [ ] Verificar a consistência interna dos dados (ex: se `CONSUMO_CAFE_BIN` == 0, então `CAFE_DIAS_SEMANA_NUM` deve ser NaN).

1.5. **Análise Exploratória de Dados (AED) Aprofundada e Visualização:**
    *   [ ] Criar um script/notebook Jupyter (`analise_exploratoria.ipynb`) dedicado.
    *   [ ] Calcular estatísticas descritivas detalhadas para todas as variáveis relevantes em `IC_Dados_Processados.csv`.
        *   Para numéricas: média, mediana, moda, DP, mínimo, máximo, quartis.
        *   Para categóricas: frequências absolutas e relativas.
    *   [ ] Gerar um conjunto rico de visualizações:
        *   Histogramas, densidades e boxplots para variáveis numéricas (`IDADE`, `MG_CAFEINA_SEMANA/DIA`, `HORAS_JOGO_PRINCIPAL_MEDIA_DIA`, etc.).
        *   Gráficos de barras para variáveis categóricas (`GENERO_COD`, `NIVEL_EDUC_COD`, `NIVEL_JOGADOR_COD`, dummies, etc.).
        *   Tabelas de contingência (crosstabs) e gráficos de barras agrupadas/empilhadas para explorar relações bivariadas entre variáveis categóricas (ex: `NIVEL_JOGADOR_COD` vs. `CONSUMO_CAFE_BIN`).
        *   Boxplots agrupados para comparar distribuições de variáveis numéricas entre grupos categóricos (ex: `MG_CAFEINA_DIA` por `NIVEL_JOGADOR_COD`).
        *   Mapas de calor de correlação (Pearson para numéricas, Cramer's V ou similar para categóricas se aplicável).
    *   [ ] Identificar e documentar padrões, tendências, outliers significativos e relações notáveis.
    *   [ ] Formular hipóteses preliminares robustas para a análise estatística.
    *   **Entregável Chave:** `analise_exploratoria.ipynb` com todos os códigos, resultados, e visualizações. Um documento sumário (ex: `AED_Resultados_Chave.md`) com os principais insights da AED.

**Fase 2: Análise Estatística e Formulação de Resultados**

2.1. **Definição Final das Questões de Pesquisa e Hipóteses Estatísticas:**
    *   [ ] Com base nos insights da AED e nos objetivos delineados em `RelatórioFinal_Éllis.md`, refinar e finalizar as questões de pesquisa centrais e secundárias.
    *   [ ] Formular hipóteses estatísticas claras, específicas e testáveis (H0 e H1) para cada questão.
        *   *Exemplos (a refinar):*
            *   "O consumo médio de cafeína (mg/dia) difere significativamente entre os diferentes níveis de jogadores de e-sports (Amador, Semi-Profissional, Profissional)?"
            *   "Existe uma correlação estatisticamente significativa entre as horas médias de jogo por dia e a quantidade de cafeína consumida?"
            *   "A proporção de indivíduos que relatam efeitos adversos da cafeína é maior entre aqueles com maior consumo?"

2.2. **Seleção e Aplicação de Testes Estatísticos Apropriados:**
    *   [ ] Escolher os testes estatísticos mais adequados com base no tipo de variáveis (nominais, ordinais, intervalares/racionais), na distribuição dos dados (paramétricos vs. não-paramétricos) e nas hipóteses.
        *   Possíveis testes: Teste t de Student (amostras independentes/pareadas), ANOVA (one-way, two-way), Teste do Qui-quadrado (independência, aderência), Correlação de Pearson (r) ou Spearman (rho), Regressão Linear Simples/Múltipla, Regressão Logística.
    *   [ ] Realizar as análises no script/notebook `analise_estatistica.ipynb` (pode ser o mesmo da AED ou um novo). Utilizar bibliotecas como `scipy.stats`, `statsmodels`.
    *   [ ] Documentar a justificativa para a escolha de cada teste.
    *   [ ] Interpretar cuidadosamente os resultados: valores de p, estatísticas de teste, graus de liberdade, intervalos de confiança, tamanhos de efeito (ex: d de Cohen, eta-quadrado, odds ratio).
    *   **Entregável Chave:** `analise_estatistica.ipynb` com todos os testes, códigos, saídas e interpretações preliminares.

2.3. **Visualização Avançada dos Resultados Estatísticos:**
    *   [ ] Gerar gráficos e tabelas de alta qualidade, prontos para publicação, que apresentem os resultados estatísticos de forma clara, concisa e visualmente apelativa.
        *   Ex: Gráficos de barras com barras de erro (IC 95%), scatter plots com linhas de regressão e bandas de confiança, tabelas formatadas com resultados dos testes.
    *   **Entregável Chave:** Conjunto de figuras (em formato vetorial como SVG/PDF ou alta resolução PNG) e tabelas (formatadas, prontas para Word/LaTeX).

2.4. **Interpretação Detalhada e Síntese dos Resultados:**
    *   [ ] Consolidar todos os achados estatisticamente significativos (e os não significativos importantes).
    *   [ ] Relacionar os resultados diretamente com cada questão de pesquisa e hipótese.
    *   [ ] Começar a esboçar a seção de "Resultados" do artigo.

**Fase 3: Redação do Artigo Científico**

3.1. **Planejamento e Estruturação do Manuscrito (Padrão IMRaD):**
    *   [x] **Título:** Finalizar o título para ser informativo, conciso e atrativo.
    *   [x] **Resumo (Abstract):** Escrever após ter as seções principais (aprox. 250-300 palavras). Incluir: breve Contexto, Objetivo principal, Métodos resumidos, Principais Resultados, Conclusões chave.
    *   [x] **Palavras-chave:** Selecionar 3-5 palavras-chave descritivas (ex: cafeína, e-sports, jogadores, hábitos de consumo, Brasil).
    *   [x] **Introdução:**
        *   Contextualizar o tema: crescimento dos e-sports, papel da cafeína como psicoestimulante, preocupações com saúde e performance.
        *   Revisão da literatura: o que já se sabe sobre consumo de cafeína em atletas, estudantes, e (se houver) jogadores de e-sports. Citar estudos relevantes.
        *   Identificar a lacuna na literatura que seu estudo preenche (ex: poucos dados sobre jogadores brasileiros, análise detalhada de múltiplos fatores).
        *   Apresentar claramente os objetivos do estudo e as questões de pesquisa/hipóteses principais.
    *   [ ] **Métodos:**
        *   Desenho do estudo: Estudo transversal descritivo e analítico, baseado em dados de questionário.
        *   População e Amostra: Descrever as características dos participantes com base nos dados (após filtro de consentimento). Detalhar o processo de recrutamento original (conforme `RelatórioFinal_Éllis.md`).
        *   Instrumento de Coleta de Dados: Descrever brevemente o questionário original, suas seções principais. Referenciar `RelatórioFinal_Éllis.md` para o questionário completo, se necessário.
        *   Processamento e Análise de Dados:
            *   Resumir as etapas chave de limpeza, transformação e codificação de dados (referenciar o `Livro_de_Codigos.txt` para detalhes).
            *   Listar as principais variáveis dependentes e independentes utilizadas na análise estatística.
            *   Descrever os testes estatísticos empregados, o software (Python com pandas, scipy.stats, statsmodels) e o nível de significância (α, usualmente 0.05).
        *   Considerações Éticas: Mencionar a aprovação por comitê de ética (se houve para a coleta original), o consentimento informado dos participantes (filtrado no processamento) e a anonimização dos dados.
    *   [ ] **Resultados:**
        *   Apresentar os achados de forma clara, lógica e objetiva, sem interpretação ou discussão nesta seção.
        *   Começar com a descrição da amostra (características demográficas, hábitos de jogo, etc., com base nas estatísticas descritivas da AED).
        *   Apresentar os resultados dos testes estatísticos para cada hipótese, referenciando as tabelas e figuras preparadas.
        *   Usar texto para guiar o leitor através dos resultados chave nas tabelas/figuras.
    *   [ ] **Discussão:**
        *   Retomar os principais achados do estudo e interpretá-los à luz das questões de pesquisa.
        *   Comparar os resultados com os de estudos anteriores (semelhanças, diferenças, possíveis explicações).
        *   Discutir as implicações teóricas e práticas dos achados (ex: para saúde dos jogadores, recomendações, desenvolvimento de políticas).
        *   Reconhecer as limitações do estudo (ex: amostra de conveniência, dados auto-relatados, desenho transversal não permite inferir causalidade).
        *   Sugerir direções para pesquisas futuras.
    *   [ ] **Conclusão:**
        *   Resumir as principais conclusões do estudo de forma concisa.
        *   Responder diretamente aos objetivos propostos na introdução.
        *   Evitar novas informações ou especulações não fundamentadas nos resultados.
    *   [ ] **Agradecimentos (Opcional):** Agradecer a agências de fomento, indivíduos que auxiliaram, etc.
    *   [ ] **Referências:** Listar todas as fontes citadas no texto, formatadas consistentemente de acordo com as normas do periódico alvo.
    *   [ ] **Apêndices (Opcional):** Incluir materiais suplementares como o questionário completo (se não detalhado no `RelatórioFinal_Éllis.md` e relevante), ou tabelas muito extensas. O `Livro_de_Codigos.txt` pode ser referenciado como material suplementar online.
    *   [ ] **Citações e Bibliografia:** Utilizar apenas fontes científicas validadas (publicações de 2023–2025); empregar RAG em bases indexadas (PubMed, Scopus, Web of Science) e manter bibliografia em formato BibTeX.

3.2. **Cronograma de Redação (Sugestão Flexível):**
    *   [ ] Semanas 1-2: Rascunho inicial de Métodos e Resultados (utilizando Fases 1 e 2 como base).
    *   [ ] Semana 3: Pesquisa bibliográfica intensiva e rascunho da Introdução.
    *   [ ] Semana 4: Rascunho da Discussão.
    *   [ ] Semana 5: Rascunho do Resumo, Conclusão, Título. Primeira revisão completa do manuscrito.

3.3. **Revisão Bibliográfica Contínua:**
    *   [ ] Utilizar bases como Google Scholar, PubMed, Scielo, Web of Science, Scopus.
    *   [ ] Focar em palavras-chave como: "caffeine consumption esports", "gaming habits caffeine", "esports player health Brazil", "stimulant use gamers", "video game addiction caffeine".
    *   [ ] Manter um registro organizado das referências (ex: usando Zotero, Mendeley).

**Fase 4: Revisão, Submissão e Pós-Submissão**

4.1. **Revisão Interna e por Pares:**
    *   [ ] Múltiplas rodadas de auto-revisão: clareza, lógica, gramática, ortografia, estilo científico, consistência.
    *   [ ] Verificar se todas as tabelas e figuras estão corretamente numeradas, legendadas e citadas.
    *   [ ] Checar a formatação das referências contra as normas do periódico alvo.
    *   [ ] **Crucial:** Pedir feedback a colegas, orientador(es), ou outros pesquisadores com experiência na área ou em publicação.

4.2. **Seleção Final do Periódico e Formatação:**
    *   [ ] Com base nos resultados finais e no escopo do artigo, selecionar o periódico alvo mais adequado.
    *   [ ] Ler atentamente e seguir rigorosamente as "Instruções para Autores" do periódico escolhido (limite de palavras, estrutura, formatação de referências, figuras, etc.).

4.3. **Preparação dos Materiais de Submissão:**
    *   [ ] Manuscrito final formatado.
    *   [ ] Carta de Apresentação (Cover Letter): Direcionada ao editor do periódico, destacando a originalidade, relevância do estudo e adequação ao escopo da revista. Declarar que o trabalho é original e não está sob consideração em outro lugar.
    *   [ ] Arquivos de figuras e tabelas nos formatos exigidos.
    *   [ ] Possíveis declarações de conflito de interesse, contribuição dos autores, etc., conforme exigido.

4.4. **Submissão Online:**
    *   [ ] Realizar a submissão através do sistema online do periódico.

4.5. **Processo Pós-Submissão:**
    *   [ ] Aguardar o feedback dos revisores (pode levar semanas ou meses).
    *   [ ] Se receber uma decisão de "Revisar e Ressubmeter" (Major/Minor Revisions):
        *   Analisar cuidadosamente todos os comentários dos revisores.
        *   Preparar uma carta resposta detalhada, abordando cada ponto levantado pelos revisores e explicando as alterações realizadas no manuscrito.
        *   Revisar o manuscrito conforme necessário.
        *   Ressubmeter o manuscrito revisado e a carta resposta.
    *   [ ] Se "Aceito": Comemorar! Seguir as instruções para provas e publicação.
    *   [ ] Se "Rejeitado": Analisar os motivos, considerar as críticas para melhorar o trabalho e selecionar um novo periódico.

**Recursos Chave do Projeto Existentes:**
*   `IC_Dados_Curados - Worksheet (1).csv`
*   `RelatórioFinal_Éllis.md` (fundamental para Métodos, Introdução e base do Livro de Códigos)
*   `src/data_processing.py` (a ser completado)
*   `requirements.txt`
*   `README.md` (visão geral do projeto técnico)

**Considerações Éticas a Serem Mantidas e Reportadas no Artigo:**
*   Confidencialidade e anonimato dos participantes.
*   Consentimento Livre e Esclarecido (TCLE) como critério de inclusão.
*   Se aplicável, menção à aprovação do projeto original por Comitê de Ética em Pesquisa.

**Próximos Passos Imediatos (Retomada do Processamento de Dados):**
1.  [ ] **Focar na Fase 1.1 e 1.2:** Implementar todas as codificações restantes em `src/data_processing.py` e desenvolver a geração do `Livro_de_Codigos.txt` detalhado.
2.  [ ] Após a conclusão do processamento, proceder com a AED (Fase 1.5).
