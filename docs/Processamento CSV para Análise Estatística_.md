# **Processamento e Tabulação Numérica de Dados de Questionário de Iniciação Científica para Análise Estatística**

## **1.0 Introdução**

### **1.1. Objetivo do Projeto**

Este relatório detalha a metodologia e a execução do processamento dos dados brutos de um questionário, provenientes do arquivo IC\_Dados\_Curados \- Worksheet (1).csv.1 O objetivo principal é transformar estes dados em um formato numérico codificado, adequado para análise estatística rigorosa utilizando Python e a biblioteca Pandas. Esta transformação abrange a limpeza dos dados, filtragem de participantes, remoção ou anonimização de Informações de Identificação Pessoal (PII), e a aplicação de regras de codificação específicas conforme os requisitos da pesquisa.

### **1.2. Fonte dos Dados de Entrada**

A única fonte de dados para esta tarefa de processamento é o arquivo CSV intitulado IC\_Dados\_Curados \- Worksheet (1).csv 1, doravante referido como o "arquivo de dados brutos".

### **1.3. Entregáveis Principais**

O resultado deste processo consistirá em dois arquivos principais:

* Um arquivo CSV processado (denominado IC\_Dados\_Processados.csv) contendo os dados numericamente codificados, com codificação UTF-8 e delimitadores de vírgula.  
* Um livro de códigos abrangente (denominado Livro\_de\_Codigos.txt) detalhando a transformação de cada variável, o esquema de codificação e quaisquer pressupostos relevantes.

### **1.4. Abordagem Metodológica**

O processamento dos dados segue uma abordagem estruturada:

* Carregamento dos dados brutos.  
* Filtragem dos participantes com base no consentimento explícito.  
* Tratamento de PII por exclusão ou anonimização.  
* Transformação de campos de data (por exemplo, cálculo da idade).  
* Limpeza e conversão de dados numéricos (por exemplo, padronização de separadores decimais, tratamento de erros).  
* Aplicação de regras sistemáticas de codificação para converter respostas categóricas e textuais em representações numéricas. Isso inclui a criação de novas variáveis, como variáveis dummy para questões de múltipla resposta.  
* Representação consistente de dados ausentes ou não codificáveis usando NaN (Not a Number).

### **1.5. Aderência às Diretrizes**

Os procedimentos aqui descritos seguem estritamente a consulta detalhada do usuário. Onde aplicável, a orientação também é extraída do documento fornecido 'Dados tabulados para análise estatística\_.pdf' 1, especialmente no que diz respeito às boas práticas gerais na tabulação de dados para pesquisa. No entanto, as regras de codificação específicas e os formatos de saída da consulta atual do usuário têm precedência (por exemplo, usando NaN para valores ausentes em vez de \-999, como observado em 1). A utilização de NaN alinha-se com as práticas padrão da biblioteca Pandas para representar dados ausentes, facilitando as operações estatísticas subsequentes. A referência a 1 é mantida para demonstrar a consideração de suas diretrizes gerais, como a estratégia de remoção de PII e a estrutura geral do livro de códigos, onde estas se alinham com as solicitações primárias do usuário.

## **2.0 Metodologia de Processamento e Codificação de Dados**

Esta seção elabora cada etapa realizada para transformar os dados brutos em um formato pronto para análise.

### **2.1. Carregamento de Dados e Filtragem Inicial: Consentimento dos Participantes**

* **Ação:** O arquivo de dados brutos IC\_Dados\_Curados \- Worksheet (1).csv 1 é carregado em um DataFrame Pandas.  
* **Lógica de Filtragem:** Um passo inicial crítico envolve a filtragem do conjunto de dados para reter apenas os registros onde a coluna 'TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO (TCLE)' contém a string exata 'Aceito'. Este passo é fundamental para garantir a conformidade com os princípios éticos da pesquisa.1 Todas as outras respostas nesta coluna (por exemplo, 'Não Aceito', em branco, ou qualquer outra variação) resultarão na exclusão do registro completo do participante do conjunto de dados processado.  
* **Tratamento da Coluna 'TCLE':** Após a filtragem, a coluna 'TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO (TCLE)' será codificada em uma nova coluna binária TCLE\_ACEITE, onde 'Aceito' é codificado como 1\. Embora todos os participantes no conjunto de dados final tenham o valor 1 para esta nova variável, sua inclusão serve como um campo de verificação confirmando a aplicação do filtro. A retenção de uma versão codificada é uma boa prática para o rastreamento dos dados. O número de participantes restantes após este filtro definirá o tamanho final da amostra para análise. Qualquer redução significativa neste ponto pode ter implicações para o poder estatístico, uma consideração analítica que, embora importante, está além do escopo do processamento de dados em si.

### **2.2. Exclusão e Anonimização de Informações de Identificação Pessoal (PII)**

* **Identificadores Diretos para Exclusão:**  
  * A coluna 'E-mail (para o envio do TCLE)' é inteiramente removida do conjunto de dados para proteger a privacidade dos participantes, conforme instrução do usuário e diretrizes éticas padrão.1  
  * A coluna 'Como você prefere ser chamado(a/e)?' também é inteiramente removida, pois contém identificadores pessoais diretos.1 A opção do usuário de anonimizar (ex: Participante\_1) foi considerada, mas a exclusão completa foi escolhida para uma proteção mais rigorosa das PII, dado que uma coluna 'ID' única é mantida.  
* **ID do Participante:** A coluna original 'ID', gerada pelo sistema de coleta de dados 1, é preservada. Esta coluna serve como um identificador alfanumérico único e não nominal para cada participante, crucial para o gerenciamento de dados e ligação de registros dentro do conjunto de dados anonimizado, sem revelar a identidade pessoal.1 A remoção de PII é um procedimento padrão e inegociável na ética em pesquisa. A manutenção de um 'ID' único e não identificador é crítica para a integridade dos dados, permitindo aos pesquisadores rastrear respostas ou fundir com outros conjuntos de dados (anonimizados) relacionados ao mesmo participante sem comprometer a confidencialidade.

### **2.3. Tratamento de Datas e Timestamps**

* **Cálculo da Idade (IDADE):**  
  * **Coluna Original:** 'Data de Nascimento' (formato esperado DD/MM/AAAA, conforme 1, e entradas típicas em 1).  
  * **Nova Coluna:** IDADE.  
  * **Transformação:** As strings da 'Data de Nascimento' serão analisadas e convertidas em objetos datetime. A idade será calculada como o número de anos completos entre a data de nascimento e uma data de referência fixa.  
  * **Data de Referência para Cálculo da Idade:** Para garantir a reprodutibilidade, a data de referência será a data da resposta mais recente registrada na coluna 'Data' (timestamp da resposta) do conjunto de dados bruto.1 Esta escolha será explicitamente documentada no livro de códigos. O uso da "data atual" é evitado, pois produziria idades diferentes se o script fosse executado novamente em uma data posterior.  
  * **Tratamento de Erros:** Se 'Data de Nascimento' estiver ausente, não puder ser analisada ou for inválida, o valor correspondente em IDADE será NaN.  
* **Timestamp da Resposta (Data):**  
  * **Coluna Original:** 'Data' (timestamp da resposta).  
  * **Novo Nome da Coluna:** TIMESTAMP\_RESPOSTA (para torná-la mais descritiva e compatível com Python).  
  * **Transformação:** As strings de timestamp originais (ex: "2023-12-04 16:23:55" de 1) serão analisadas e padronizadas para o formato YYYY-MM-DD HH:MM:SS, dado que o tempo está consistentemente presente e pode ser relevante. Esta padronização assegura consistência para qualquer análise baseada no tempo. A conversão de datas de nascimento para IDADE cria uma variável contínua ou ordinal prontamente utilizável para análise demográfica. A padronização de timestamps é crucial para quaisquer análises que envolvam o tempo de resposta ou duração. A escolha de uma data de referência fixa para o cálculo da idade é um detalhe metodológico chave para a reprodutibilidade.

### **2.4. Limpeza e Conversão de Dados Numéricos**

* **Colunas Alvo:** 'Mg cafeína semana', 'Mg cafeína dia', 'Mg homens', 'Mg mulheres'. Estas colunas são identificadas na consulta e em 1 como necessitando de limpeza.  
* **Transformações:**  
  1. **Separador Decimal:** Todas as ocorrências de vírgula (,) como separador decimal serão substituídas por um ponto (.) (ex: "942,6" torna-se "942.6"). Isto é essencial para a correta interpretação numérica pelo Pandas.1  
  2. **Conversão de Tipo:** Após a limpeza, as colunas serão convertidas para um tipo numérico de ponto flutuante (float).  
  3. **Tratamento de Erros:**  
     * Valores que estão vazios/em branco no CSV original serão convertidos para NaN.  
     * Valores de texto não numéricos, especificamente "\#ERROR\!" (observado em 1 para 'Mg mulheres' e notado em 1), serão convertidos para NaN. Qualquer outro texto não conversível também se tornará NaN.  
* **Novos Nomes de Colunas:** As colunas processadas serão nomeadas MG\_CAFEINA\_SEMANA, MG\_CAFEINA\_DIA, MG\_HOMENS, MG\_MULHERES, seguindo uma convenção de nomenclatura consistente (maiúsculas com underscores, conforme sugerido pelos exemplos da consulta e o estilo de 1).  
* **Sem Recálculo:** É explicitamente notado, conforme solicitação do usuário e 1, que estes valores de cafeína são considerados como reportados pelos participantes (ou de cálculos prévios nos dados brutos) e são apenas limpos e padronizados, não recalculados usando bancos de dados de referência de cafeína externos como.1 Esta limpeza garante que estas variáveis sejam verdadeiramente numéricas e possam ser usadas em cálculos estatísticos (médias, correlações, etc.). A presença de valores "\#ERROR\!" nos dados brutos 1 sublinha a necessidade de um tratamento de erros robusto durante a conversão. A renomeação das colunas para um formato padronizado facilita a sua utilização em scripts Python.

### **2.5. Estratégia de Codificação de Variáveis Categóricas e Textuais**

Esta subseção detalha a conversão de respostas textuais e categóricas em códigos numéricos.

* **2.5.1. Princípios Gerais para Codificação Categórica:**  
  * **Padronização de Texto:** Antes de qualquer codificação numérica, todas as respostas textuais passarão por padronização:  
    * Conversão para um caso consistente (minúsculas será utilizado para facilitar a correspondência).  
    * Remoção de espaços em branco no início e no fim.  
    * Normalização de variações comuns (ex: "Nao" para "Não", tratamento de "estudante" e "Estudante" para o mesmo código, conforme 1).  
  * **Convenção de Nomenclatura para Novas Colunas:**  
    * Variáveis binárias (Sim/Não): \_BIN (ex: CONSUMO\_CAFE\_BIN).  
    * Variáveis codificadas nominais ou ordinais: \_COD (ex: GENERO\_COD, NIVEL\_EDUC\_COD).  
    * Variáveis numericamente extraídas/convertidas: \_NUM (ex: CAFE\_DIAS\_SEMANA\_NUM) ou \_ (ex: CAFE\_RECIPIENTE\_VOL\_ML).  
    * Variáveis dummy de múltipla escolha: \_.  
  * **Representação de Valores Ausentes:** Respostas não codificáveis, strings vazias ou questões explicitamente puladas (onde não uma categoria definida como "Prefiro não responder") serão codificadas como NaN nas colunas numéricas processadas, conforme a instrução primária do usuário.  
* **2.5.2. Regras de Codificação Específicas para Variáveis:**  
  * **Gênero \-\> GENERO\_COD**  
    * **Coluna Original:** 'Gênero'  
    * **Codificação (Nominal):** 'Masculino': 1, 'Feminino': 2, 'Prefiro não responder': 3, 'Não-binário': 4\. Outros/Ausentes: NaN. (Fonte: Consulta do usuário; 1; 1 para frequências: Masculino (48), Feminino (12), Prefiro não responder (3), Não-binário (3)). A inclusão explícita de "Prefiro não responder" e "Não-binário" como categorias distintas é importante para a coleta e análise de dados inclusivas, refletindo práticas contemporâneas em pesquisa.  
  * **Nível de educação \-\> NIVEL\_EDUC\_COD**  
    * **Coluna Original:** 'Nível de educação'  
    * **Codificação (Ordinal):** Com base nas frequências de 1 ('Ensino superior incompleto': 37, 'Pós-graduação': 17, 'Ensino médio completo': 12, 'Ensino superior completo': 2\) e na ordem desejada pela consulta:  
      * 'Ensino médio completo': 1 (Dado que 'Ensino médio incompleto', mencionado na consulta, não aparece em 1, o nível mais baixo observado inicia a codificação).  
      * 'Ensino superior incompleto': 2  
      * 'Ensino superior completo': 3  
      * 'Pós-graduação': 4 Outros/Ausentes: NaN. (Fonte: Consulta do usuário; 1; 1). Preservar a natureza ordinal permite análises que respeitam a progressão ordenada dos níveis educacionais. Os valores únicos reais de 1 ditarão a escala de codificação final, garantindo que todos os dados observados sejam capturados e devidamente documentados no livro de códigos.  
  * **Em qual nível você se classifica como jogador de esportes eletrônicos? \-\> NIVEL\_JOGADOR\_COD**  
    * **Codificação (Ordinal):** 'Amador/Jogador casual': 1, 'Semi-Profissional': 2, 'Profissional': 3\. Outros/Ausentes: NaN. (Fonte: Consulta do usuário; 1; 1 para frequências: Amador/Jogador casual (50), Semi-Profissional (15), Profissional (2)). Esta variável fornece uma medida subjetiva do nível de habilidade/engajamento do jogador, que pode ser correlacionada com hábitos de jogo ou consumo de cafeína.  
  * **Você consome café? \-\> CONSUMO\_CAFE\_BIN**  
    * **Codificação (Binária):** 'Sim': 1, 'Não': 0\. Outros/Ausentes: NaN. (Fonte: Consulta do usuário; 1). Esta é uma pergunta de entrada crucial para questões subsequentes relacionadas ao café. Sua codificação precisa é vital para análises condicionais; por exemplo, se a resposta for 'Não' (código 0), variáveis dependentes como CAFE\_DIAS\_SEMANA\_NUM deverão ser NaN para esse participante.  
  * **Quantos dias por semana você consome café? \-\> CAFE\_DIAS\_SEMANA\_NUM**  
    * **Codificação (Numérica/Ordinal):** 'Raramente': 0.5 (consistente com a sugestão da consulta para um valor baixo, não nulo, representando consumo infrequente), '1-2 vezes por semana': 1.5, '3-4 vezes por semana': 3.5, '5-6 vezes por semana': 5.5, 'Todos os dias': 7\. 'Nunca' (se presente e distinto de não consumidores): 0\. Outros/Ausentes: NaN. (Fonte: Consulta do usuário; 1 usa códigos ordinais; 1 para frequências. 'Nunca' não está em 1, sugerindo que é tratado por CONSUMO\_CAFE\_BIN ser 0). A utilização de pontos médios para intervalos permite que esta variável seja tratada como pseudo-contínua, embora as categorias subjacentes sejam ordinais. A escolha de 0.5 para 'Raramente' será claramente documentada. Se um participante respondeu 'Não' para CONSUMO\_CAFE\_BIN, então CAFE\_DIAS\_SEMANA\_NUM será NaN.  
  * **Em qual tipo de recipiente você costuma consumir seu café? \-\> CAFE\_RECIPIENTE\_VOL\_ML**  
    * **Ação:** Extrair o valor numérico de mL. Ex: "Xícara pequena: 50 ml" \-\> 50; "Caneca média: 300 ml" \-\> 300\. "Cápsula (Café preparado usando máquinas que funcionam com cápsulas pré-preparadas)" \-\> NaN, pois nenhum volume é especificado. (Fonte: Consulta do usuário; 1; 1). Esta transformação cria uma medida quantitativa do volume de consumo típico por instância, essencial para quaisquer cálculos futuros de dosagem de cafeína. A análise de 1 confirma que a maioria das opções de resposta para esta pergunta inclui explicitamente valores em mL, facilitando a extração.  
  * **"Com base no recipiente que você selecionou anteriormente ( \_\_\_ ""), quantas vezes no dia você consome café nesse recipiente?" \-\> CAFE\_VEZES\_DIA\_NUM**  
    * **Ação:** Extrair o valor numérico. Ex: "1 vez ao dia" \-\> 1; "5 vezes ou mais ao dia" \-\> 5\. Outros/Ausentes: NaN. (Fonte: Consulta do usuário; 1). Fornece uma contagem de frequência diária para o recipiente especificado, outro componente chave para cálculos potenciais de consumo total. A resposta "5 vezes ou mais ao dia" será codificada como 5, e esta interpretação será documentada.  
  * **Qual tipo de café você mais costuma consumir? \-\> CAFE\_TIPO\_PRINCIPAL\_COD**  
    * **Ação:** Mapear tipos únicos para códigos numéricos. 1 e 1 listam tipos como 'Expresso', 'Coado', 'Cápsula'. A resposta "1 coado e 1 de cápsula por dia" (de 1) será atribuída a um código único se aparecer nos dados de 1 para esta pergunta; caso contrário, esta resposta complexa específica será anotada como necessitando de tratamento especial se encontrada. Os textos serão padronizados (ex: remoção de descrições entre parênteses se o tipo base for claro e distinto, ou mantidos se diferenciarem tipos como "Expresso (Café forte...)" vs. apenas "Expresso", caso ambos apareçam) antes da atribuição de códigos inteiros sequenciais.  
    * **Insight:** Categoriza o tipo primário de café, permitindo a análise de preferências. Respostas mistas como "1 coado e 1 de cápsula" destacam a complexidade do autoconsumo relatado e a necessidade de uma estratégia de codificação flexível ou a criação de categorias combinadas.  
  * **"Quantas horas por dia, em média, você joga e-sports?" (1ª e 2ª ocorrências) \-\> HORAS\_JOGO\_PRINCIPAL\_MEDIA\_DIA e HORAS\_JOGO\_OUTROS\_MEDIA\_DIA**  
    * **Nomenclatura:** Seguindo a lógica inferida de 1 e a posição das perguntas no questionário (Q22 após "Qual(is) outro(s) você joga?"), serão criadas duas colunas distintas para capturar as horas dedicadas ao jogo principal e a outros jogos, respectivamente.  
    * **Codificação (Híbrida Numérica/Ordinal):**  
      * 'Menos de 1 hora': 0.5  
      * '1-2 horas': 1.5  
      * '2-4 horas' (e "3 HORAS" de 1/1): 3.0  
      * '4-6 horas' (e "Não jogo diariamente, mas qnd jogo é entre 4-6 horas" de 1/1): 5.0  
      * 'Mais de 6 horas': 7.0 (Conforme sugestão da consulta, será usado 7.0 e documentado).  
      * 'Jogo somente aos finais de semana': Para as colunas numéricas de média diária (\_MEDIA\_DIA), esta categoria será codificada como NaN, pois não representa uma média diária consistente de quem joga regularmente durante a semana. Será documentado que este NaN representa um padrão de jogo não diário. 1 atribui um código ordinal (6), o que seria apropriado para uma variável puramente ordinal, mas a consulta prioriza a conversão numérica para média diária.  
      * 'Não jogo todo dia atualmente': Similarmente, será NaN nas colunas \_MEDIA\_DIA. 1 codifica como 7\.  
      * 'Costumava jogar 8 horas por dia quando a grade horária da faculdade não era tão pesada, Hoje, com sorte, jogo 40 minutos por dia': A parte relevante para o consumo atual ("Hoje, com sorte, jogo 40 minutos por dia") será convertida para aproximadamente 0.67 horas. Se apenas a parte do "costumava jogar" estiver presente sem uma indicação atual, será NaN. 1 codifica como 8, focando na resposta textual completa.  
      * 'xx' (de exemplo em 1): NaN.  
      * Outros/Ausentes: NaN.  
    * **Fonte:** Consulta do usuário.1 A distinção entre horas de jogo para o jogo principal e "outros" jogos, conforme sugerido pela estrutura do questionário e pelos nomes de variáveis em 1, é uma nuance importante que será preservada. A conversão para valores numéricos que representam médias diárias é priorizada, mas o tratamento de respostas que não se encaixam diretamente nesse esquema (como "jogo somente aos finais de semana") requer uma abordagem cuidadosa, resultando em NaN para as colunas de média diária e uma nota explicativa no livro de códigos.  
  * **Qual a dose que você toma de cafeína em suplemento por dia? \-\> SUPLEM\_DOSE\_CAFEINA\_MG e SUPLEM\_DOSES\_NUM**  
    * **Ação:**  
      * Respostas como "200mg", "400mg": O valor numérico será extraído para SUPLEM\_DOSE\_CAFEINA\_MG. SUPLEM\_DOSES\_NUM será 1 (assumindo uma porção) ou NaN.  
      * Respostas como "1 dose", "2 doses": SUPLEM\_DOSES\_NUM receberá 1 ou 2\. SUPLEM\_DOSE\_CAFEINA\_MG será NaN, a menos que uma conversão padrão de mg/dose (ex: 200mg por dose, conforme exemplo da consulta) seja explicitamente aplicada e documentada. Sem uma fonte de conversão confiável e universal para "dose", manter a informação em SUPLEM\_DOSES\_NUM e NaN em SUPLEM\_DOSE\_CAFEINA\_MG é a abordagem mais segura.  
      * "dose extremamente baixa no multi vitamínico": SUPLEM\_DOSE\_CAFEINA\_MG \= NaN (a menos que uma estimativa numérica baixa, como 5mg, possa ser justificada e documentada). SUPLEM\_DOSES\_NUM \= NaN. 1 codifica esta resposta textualmente como categoria 5; para a conversão numérica, NaN é mais apropriado se a quantificação for incerta.  
      * "Não tenho acesso ao pote no momento": SUPLEM\_DOSE\_CAFEINA\_MG \= NaN, SUPLEM\_DOSES\_NUM \= NaN. 1 codifica como categoria 6\.  
      * "300/400mg": SUPLEM\_DOSE\_CAFEINA\_MG \= 350 (ponto médio). SUPLEM\_DOSES\_NUM \= NaN ou 1\. 1 codifica como categoria 7\.  
      * "1" (genérico, provavelmente referindo-se a 1 dose/cápsula): SUPLEM\_DOSES\_NUM \= 1\. SUPLEM\_DOSE\_CAFEINA\_MG \= NaN. 1 codifica como categoria 8\.  
    * **Fonte:** Consulta do usuário1/.1 Este campo exige uma análise cuidadosa e sensível ao contexto. A criação de duas colunas separadas, SUPLEM\_DOSE\_CAFEINA\_MG e SUPLEM\_DOSES\_NUM, conforme sugerido pela consulta, é uma estratégia robusta para lidar com os tipos de resposta mistos, especialmente quando uma conversão direta para mg não é consistentemente possível.  
* **2.5.3. Questões de Múltipla Escolha para Variáveis Dummy:**  
  * **Questões Alvo:**  
    * 'Em quais momentos do dia você costuma consumir café?' (1)  
    * 'Que tipo(s) de chocolate você consome mais frequentemente?' (1)  
    * 'Qual(is) outro(s) você joga?' (1)  
    * '"Além da sua plataforma principal ( \_\_\_ ), Você joga em outra?"' (1)  
    * 'Qual outro tipo de café você costuma consumir?' (1)  
    * 'Em quais momentos do dia você costuma consumir energético?' (1)  
    * '"Além do seu chá principal ( \_\_\_ ), você consome outro tipo de chá?"' (1)  
    * 'Em quais momentos do dia você costuma consumir seu chá?' (1)  
    * 'Em quais momentos do dia você costuma consumir refrigerante a base de cola?' (1)  
    * 'Em quais momentos do dia você costuma consumir o seu suplemento?' (1)  
    * '"Porque você consome alimentos, bebidas ou suplementos com cafeína?"' (1)  
  * **Metodologia:**  
    1. Para cada questão, serão agregadas todas as respostas únicas do arquivo IC\_Dados\_Curados \- Worksheet (1).csv.1 As listas de respostas combinadas (ex: de 1) serão utilizadas para identificar as opções individuais.  
    2. As strings separadas por vírgula (ou outro delimitador, se observado) serão divididas em opções individuais.  
    3. Cada opção será padronizada (minúsculas, remoção de espaços extras, tratamento de variações menores para consolidação). Por exemplo, "No café da manhã" e "no café da manhã" seriam tratadas como a mesma opção.  
    4. Será identificado o conjunto de opções padronizadas únicas para a questão. Estas formarão a base para os nomes das novas colunas dummy.  
    5. Serão criadas novas colunas binárias para cada opção única (ex: CAFE\_MOMENTO\_AO\_ACORDAR, CHOC\_TIPO\_AOLEITE, OUTROJOGO\_VALORANT). O nome da coluna seguirá o padrão \_.  
    6. Para cada participante, estas colunas dummy serão preenchidas: 1 se o participante selecionou aquela opção, 0 se não selecionou aquela opção (mas respondeu à pergunta). Se a pergunta original foi deixada em branco/NaN pelo participante, todas as variáveis dummy associadas para aquele participante também serão NaN. Esta distinção entre uma não seleção explícita (0) e uma não resposta à pergunta (NaN) é importante para a integridade da análise. A abordagem de 1, que sugere 0 se não selecionado, será seguida para os casos em que a pergunta foi respondida, mas a opção específica não foi marcada.  
  * **Exemplo para 'Em quais momentos do dia você costuma consumir café?'** 1**:**  
    * Resposta bruta de um participante: "Ao acordar, No café da manhã, Após o almoço"  
    * Opções únicas padronizadas identificadas a partir de todos os dados (exemplo): 'ao acordar', 'no café da manhã', 'meio da manhã (por volta das 10h-11h)', 'antes do almoço', 'após o almoço', 'meio da tarde (por volta das 15h-16h)', 'no jantar', 'antes de dormir', 'de madrugada (entre 22h-04h)', 'durante sessões de jogos ou treinos', 'as vezes durante o dia, em horário alternado', 'quando preciso de concentrar para um projeto'.  
    * Novas colunas: CAFE\_MOMENTO\_AO\_ACORDAR, CAFE\_MOMENTO\_NO\_CAFE\_DA\_MANHA,..., CAFE\_MOMENTO\_QUANDO\_PRECISO\_CONCENTRAR.  
    * Para o participante do exemplo: CAFE\_MOMENTO\_AO\_ACORDAR=1, CAFE\_MOMENTO\_NO\_CAFE\_DA\_MANHA=1, CAFE\_MOMENTO\_APOS\_ALMOCO=1. Todas as outras colunas CAFE\_MOMENTO\_\* para este participante \= 0\. Esta transformação é essencial para analisar preferências por opções individuais dentro de um conjunto de múltiplas respostas e é uma prática padrão em análise de dados de questionários. Resultará em um aumento considerável no número de variáveis no conjunto de dados processado, um fator que o analista deve considerar ao planejar as análises subsequentes. A documentação clara no livro de códigos, ligando cada nova variável dummy à sua pergunta original, será crucial para a interpretabilidade.  
* **2.5.4. Codificação de Variáveis Textuais de Alta Cardinalidade:**  
  * **Ocupação profissional \-\> OCUPACAO\_COD**  
    * **Estratégia:** O texto será padronizado (minúsculas, remoção de espaços). A extensa lista de ocupações e códigos de 1 será utilizada como guia principal de mapeamento. Esta lista inclui 65 categorias codificadas e um código 99 para "Outra Ocupação". Os valores únicos e frequências de 1 serão cruzados com esta lista. Respostas como "Estudante" e "estudante" serão mapeadas para o mesmo código (ex: 1, conforme 1). Respostas muito infrequentes não cobertas por 1 serão agrupadas no código 'Outra\_Ocupacao'. "N/A" ou similares serão tratados como uma categoria específica se recorrentes e codificados em 1 (ex: código 36), ou como NaN se não. Aproveitar a codificação preexistente de 1 para uma variável com tantas entradas únicas potenciais é eficiente e provavelmente se alinha com trabalhos anteriores ou expectativas do pesquisador. Qualquer nova ocupação frequente identificada em 1 e não presente em 1 será avaliada para possivelmente receber um novo código, que será devidamente documentado.  
  * **Qual é o seu jogo eletrônico principal? \-\> JOGO\_PRINCIPAL\_COD**  
    * **Estratégia:** Os nomes dos jogos serão padronizados (ex: "Counter-Strike: Global Offensive" e "Counter-Strike" podem ser agrupados se contextualmente similares, ou mantidos distintos se 1/1 assim o sugerirem; "Red Dead Redemption 2" e "Red Dead Redeption 2" serão padronizados para o mesmo nome). 1 e 1 serão usados para identificar jogos frequentemente mencionados e atribuir códigos únicos. Jogos menos frequentes serão mapeados para um Outro\_Jogo\_Principal\_COD (ex: 99 em 1). Similar à ocupação, codificar jogos populares individualmente e agrupar a "cauda longa" é uma abordagem prática para análise. A lista de 1 fornece um bom ponto de partida, que será complementado e verificado com os dados de frequência de.1  
  * **Especifique a marca do tipo de chocolate que você consome ( \_\_\_ ) \-\> CHOCOLATE\_MARCA\_COD**  
    * **Estratégia:** Esta coluna requer uma limpeza extensiva com base em.1 Os nomes das marcas serão padronizados (ex: "Nestlé", "nestle 50%" \-\> Nestle; "Cacau Show", "cacau show 70%" \-\> Cacau Show; "Hershey's", "Hersheys meio amargo" \-\> Hershey's; "Meu favorito é BIS kkkkkkkk" \-\> Bis). A lista de 1 servirá como guia. Marcas frequentes e padronizadas receberão códigos. Outras serão agrupadas em Outra\_Marca\_Chocolate\_COD (ex: 99 em 1). Respostas como "todas as marcas" ou "Várias marcas, vário" também podem ser agrupadas em uma categoria genérica ou "Outra". A alta variabilidade e a natureza de texto livre desta pergunta exigem um processo cuidadoso de padronização e categorização para criar uma variável nominal útil.  
  * **Qual(is) outro(s) você joga? \-\> Múltiplas variáveis dummy (ex: OUTROJOGO\_VALORANT\_BIN, OUTROJOGO\_MINECRAFT\_BIN)**  
    * **Estratégia:** Este é um campo de texto de múltiplas respostas. A estratégia será similar a outras questões de múltipla escolha: criação de variáveis dummy para jogos comuns identificados em 1 e.1 Jogos menos frequentes podem ser capturados em uma variável binária geral OUTROJOGO\_OUTROS\_PRESENTE ou ignorados se muito esparsos. A consulta do usuário sugere variáveis dummy. Respostas como "Nenhum" serão codificadas em uma variável OUTROJOGO\_NENHUM\_BIN. A padronização de nomes de jogos é crucial aqui (ex: "FIFA, EA FC ou PES" tratado como uma categoria combinada OUTROJOGO\_FIFA\_EAFC\_PES\_BIN ou dividido se a granularidade for desejada e os componentes forem distintos).  
  * **Qual outro tipo de café você costuma consumir? \-\> Múltiplas variáveis dummy (ex: CAFE\_OUTRO\_TIPO\_INSTANTANEO\_BIN)**  
    * **Estratégia:** Similar à questão anterior. 1 sugere variáveis dummy para tipos como 'Instantâneo', 'Cápsula'. A resposta peculiar "Refrigerantes e energéticos" (se presente nos dados de 1) será tratada como uma categoria dummy distinta (CAFE\_OUTRO\_TIPO\_REFRIGERANTES\_ENERGETICOS\_BIN). Esta abordagem permite analisar a variedade de outros tipos de café consumidos.  
  * **"Além do seu chá principal ( \_\_\_ ), você consome outro tipo de chá?" \-\> Múltiplas variáveis dummy (ex: CHA\_OUTRO\_TIPO\_VERDE\_BIN)**  
    * **Estratégia:** 1 e 1 listam vários tipos de chá (ex: 'Chá verde', 'Chá gelado (Ice tea)', 'Chá gengibre'). Cada um destes se tornará uma variável dummy. Respostas vazias ou que indiquem não consumir outros tipos resultarão em 0 para todas as dummies relacionadas (ou NaN se a pergunta principal sobre consumo de chá for 'Não').  
  * **Você faz parte de algum time ou organização de esportes eletrônicos? \-\> PARTE\_TIME\_ORG\_COD (binária) e NOME\_TIME\_ORG\_PREENCHIDO (binária)**  
    * **Estratégia:** A coluna original combina respostas "Sim/Não" com nomes de times.1  
      * PARTE\_TIME\_ORG\_COD: Será 1 se a resposta indicar participação atual ou passada (ex: "Sim", nome do time, "Fazia parte", "Hoje em dia não mais..."). Será 0 se a resposta indicar explicitamente não participação (ex: "Não", "Não faço", "Não faço parte").  
      * NOME\_TIME\_ORG\_PREENCHIDO: Será 1 se um nome de time/organização específico foi fornecido (ex: "Leaner Energy", "FEARWW"). Será 0 se a resposta foi um "Sim" genérico, "Não", ou em branco.  
    * Respostas como "Não nesse semestre" serão codificadas como 1 para PARTE\_TIME\_ORG\_COD (participação passada/intermitente) e 0 para NOME\_TIME\_ORG\_PREENCHIDO se nenhum nome for dado. A criação de duas variáveis permite capturar a nuance entre simplesmente afirmar participação e fornecer o nome de uma organização específica, o que pode ser útil para diferentes tipos de análise.  
  * **Especifique a porção média de chocolate no dia que consome ( \_\_\_ ) \-\> CHOCOLATE\_PORCAO\_COD**  
    * **Estratégia:** As respostas são altamente descritivas.1 Serão categorizadas em grupos nominais baseados nas descrições. Exemplos de categorias (a serem refinadas com base nos dados completos de 1):  
      * 1 \= "1-2 quadradinhos"  
      * 2 \= "3-4 quadradinhos"  
      * 3 \= "5-6 quadradinhos / Meia barra pequena"  
      * 4 \= "Barra pequena / 1 unidade (aprox. 20-50g)" (ex: "1 barra pequena de 40g", "2 quadradinhos(20g)")  
      * 5 \= "Barra inteira / 1 barra (aprox. 80-100g)" (ex: "1 barra", "100g")  
      * 6 \= "Colheres" (ex: "duas colheres?", "2 colheres")  
      * 7 \= "Múltiplas unidades pequenas/variadas" (ex: "dois Batons e uma barra pequena de Laka", "4 ao dia" (Bis/Sonho de Valsa))  
      * 8 \= "Variável / Grande quantidade ocasional / Não padronizado" (ex: "Se tiver 1kg, como 1kg rsrs", "Sempre me limito a 1 porção estabelecida pela embalagem por dia")  
      * 99 \= "Outra\_Porcao\_Descritiva"  
      * NaN \= Ausente/Não aplicável. A codificação será nominal devido à dificuldade de impor uma ordem estrita ou converter para uma escala numérica contínua de forma confiável. O objetivo é agrupar respostas textuais semelhantes para facilitar a análise categórica.  
  * **Para os efeitos colaterais que você sentiu ao consumir cafeína, Com que frequência eles aparecem? \-\> EFEITO\_ADVERSO\_FREQUENCIA\_DESCRITA\_COD**  
    * **Estratégia:** As respostas são textuais e muito variadas.1 O foco será extrair menções explícitas de frequência e, secundariamente, categorizar a natureza da descrição se a frequência não for clara.  
      * Serão identificadas palavras-chave de frequência (ex: "raramente", "sempre", "ocasionalmente", "nunca", "frequentemente", "depende").  
      * Códigos nominais serão atribuídos com base nessas frequências.  
        * 1 \= Raramente mencionada  
        * 2 \= Ocasionalmente mencionada  
        * 3 \= Frequentemente mencionada  
        * 4 \= Sempre mencionada  
        * 5 \= Frequência condicional/variável (ex: "Se eu tomar a noite...", "Depende da quantidade...")  
        * 6 \= Nenhuma frequência explícita mencionada, mas descrição presente  
        * 7 \= Negação de efeitos ou frequência não aplicável (ex: "Não tenho")  
        * NaN \= Ausente.  
      * Exemplos de 1: "Se eu tomar a noite café acabo tento insônia, porém evito isso" \-\> 5\. "Aparecem raramente, geralmente quando o consumo está associado ao jejum" \-\> 1 (ou 5, dependendo da ênfase na condicionalidade). "Tenho insônia sempre que consumo café a tarde" \-\> 4\. Esta abordagem tenta quantificar a frequência quando possível, mas reconhece a natureza qualitativa de muitas respostas, agrupando-as de forma significativa.  
* **2.6. Tratamento de Valores Ausentes**  
  * **Regra Geral:** Para todas as colunas no arquivo CSV processado final, os valores ausentes (células vazias no original, respostas não mapeadas ou explicitamente puladas que não constituem uma categoria de resposta válida) serão representados como NaN. Esta é uma instrução direta do usuário e é o método padrão de tratamento de ausentes no Pandas, facilitando análises subsequentes que podem automaticamente excluir ou imputar esses valores.  
  * **Exceção para Variáveis Dummy:** Conforme detalhado na seção 2.5.3, para variáveis dummy criadas a partir de questões de múltipla escolha, um valor 0 indica que a opção não foi selecionada pelo participante (assumindo que a pergunta foi respondida), enquanto NaN indicará que a pergunta original de múltipla escolha não foi respondida pelo participante.  
  * **Documentação:** O livro de códigos especificará para cada variável como os dados ausentes ou opções de não resposta específicas (por exemplo, 'Prefiro não responder', se não for uma categoria codificada separadamente para uma determinada variável) foram tratados.  
  * **Comparação com** 1**:** O documento 1 menciona o uso universal de \-999 para dados ausentes. No entanto, esta implementação seguirá a diretiva do usuário de usar NaN. A consistência na representação de dados ausentes é fundamental para a precisão da análise estatística.

## **3.0 Arquivos de Saída Gerados**

### **3.1. Arquivo CSV Processado (IC\_Dados\_Processados.csv)**

* **Descrição:** Um único arquivo CSV contendo todos os dados processados e numericamente codificados.  
* **Formato:** Delimitado por vírgula, codificação UTF-8.  
* **Conteúdo:** Cada linha representa um participante que consentiu com o TCLE. Cada coluna representa uma variável original ou recém-derivada, numericamente codificada conforme as regras detalhadas na Seção 2.0 e documentadas exaustivamente na Seção 4.0 (Livro de Códigos).  
* **Legibilidade:** Os nomes das colunas são compatíveis com Python (usando underscores para separar palavras, sem caracteres especiais) e seguem, em geral, as convenções de nomenclatura sugeridas na consulta do usuário e exemplificadas em 1 (ex: sufixos \_COD, \_BIN, \_NUM, \_ML, \_MG).

### **3.2. Arquivo do Livro de Códigos (Livro\_de\_Codigos.txt)**

* **Descrição:** Um arquivo de texto (.txt) detalhando a transformação e codificação para cada variável no arquivo IC\_Dados\_Processados.csv.  
* **Formato:** Texto simples, codificação UTF-8, para fácil leitura e portabilidade.  
* **Estrutura do Conteúdo (para cada variável):**  
  * ID\_ORIGINAL\_QUESTAO: Identificador da questão original (ex: Q1, Q2 \- baseado em 1 quando disponível, ou atribuído sequencialmente).  
  * NOME\_COLUNA\_ORIGINAL: Nome da coluna como aparece no arquivo IC\_Dados\_Curados \- Worksheet (1).csv.  
  * NOME\_VARIAVEL\_PROCESSADA(S): Nome(s) da(s) nova(s) coluna(s) no arquivo CSV processado.  
  * DESCRICAO\_VARIAVEL: Texto original da pergunta do questionário ou descrição da variável calculada/derivada.  
  * TIPO\_VARIAVEL\_ORIGINAL: Tipo da variável no arquivo original (ex: Seleção única, Texto livre, Data).  
  * TIPO\_VARIAVEL\_PROCESSADA: Tipo da variável no arquivo processado (ex: Nominal, Ordinal, Binária, Contínua/Escala, Texto, Dummy).  
  * ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Detalhamento do mapeamento de valores textuais originais para códigos numéricos, ou descrição da regra de transformação/cálculo aplicada. Para variáveis dummy, indicará que representa a seleção de uma opção específica.  
  * VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: Listagem dos valores únicos observados no arquivo original e seus respectivos códigos numéricos atribuídos no arquivo processado, informados pela análise dos dados (ex: 1, etc.). Para variáveis dummy, esta seção pode listar a opção que a dummy representa.  
  * NOTAS\_CODIFICACAO: Quaisquer pressupostos feitos durante a codificação, tratamento específico de valores atípicos ou respostas ambíguas, e como os dados ausentes (NaN) foram tratados para aquela variável específica. Referências a decisões baseadas em documentos específicos (ex: "Baseado em 1") ou na consulta do usuário. O livro de códigos é fundamental para a compreensão e utilização correta dos dados processados. Sua abrangência e clareza são vitais para permitir que o usuário realize análises estatísticas válidas e reprodutíveis. A ligação clara entre variáveis originais e processadas, especialmente no caso da criação de múltiplas variáveis dummy a partir de uma única questão de múltipla escolha, será cuidadosamente documentada. Da mesma forma, as regras para extração de valores numéricos de texto (como volumes ou doses) e o tratamento de entradas não padronizadas serão explicitadas.

## **4.0 Livro de Códigos Detalhado**

Esta seção constitui o conteúdo do arquivo Livro\_de\_Codigos.txt. Cada entrada descreve uma variável no arquivo IC\_Dados\_Processados.csv.

---

ID\_ORIGINAL\_QUESTAO: N/A (Metadado gerado pelo sistema de coleta)  
NOME\_COLUNA\_ORIGINAL: ID  
NOME\_VARIAVEL\_PROCESSADA(S): ID\_PARTICIPANTE  
DESCRICAO\_VARIAVEL: Identificador único alfanumérico para cada participante.  
TIPO\_VARIAVEL\_ORIGINAL: Texto livre (Alfanumérico)  
TIPO\_VARIAVEL\_PROCESSADA: Texto  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Mantido como está do arquivo original.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: Valores alfanuméricos únicos para cada participante.  
NOTAS\_CODIFICACAO: Esta coluna foi mantida para identificação única dos registros após a remoção de PII. Não é nominal e não deve ser usada diretamente em análises estatísticas como uma variável categórica.

---

ID\_ORIGINAL\_QUESTAO: Q1 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO (TCLE)  
NOME\_VARIAVEL\_PROCESSADA(S): TCLE\_ACEITE  
DESCRICAO\_VARIAVEL: Resposta ao Termo de Consentimento Livre e Esclarecido.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Binária  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= 'Aceito'  
* NaN \= Outros valores não mapeados ou ausentes (embora todos os participantes no dataset final devam ter 'Aceito'). **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:**  
* 'Aceito': 1 **NOTAS\_CODIFICACAO:** Apenas participantes que responderam 'Aceito' foram incluídos no conjunto de dados final. Todos os registros no arquivo processado terão valor 1 nesta coluna.

---

ID\_ORIGINAL\_QUESTAO: N/A (Metadado gerado pelo sistema de coleta)  
NOME\_COLUNA\_ORIGINAL: Data  
NOME\_VARIAVEL\_PROCESSADA(S): TIMESTAMP\_RESPOSTA  
DESCRICAO\_VARIAVEL: Timestamp da submissão da resposta do questionário.  
TIPO\_VARIAVEL\_ORIGINAL: Timestamp  
TIPO\_VARIAVEL\_PROCESSADA: Texto (formato YYYY-MM-DD HH:MM:SS)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Convertido para formato padronizado YYYY-MM-DD HH:MM:SS.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: Timestamps diversos.  
NOTAS\_CODIFICACAO: Mantido para referência temporal. A data mais recente nesta coluna foi usada como referência para o cálculo da idade.

---

ID\_ORIGINAL\_QUESTAO: N/A (Metadado gerado pelo sistema de coleta)  
NOME\_COLUNA\_ORIGINAL: Pontuação  
NOME\_VARIAVEL\_PROCESSADA(S): PONTUACAO\_ORIGINAL  
DESCRICAO\_VARIAVEL: Pontuação original do questionário (se aplicável).  
TIPO\_VARIAVEL\_ORIGINAL: Numérico/Texto  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Mantido como está, após conversão para numérico. Vírgulas decimais convertidas para pontos. Erros ou não numéricos para NaN.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: Valores numéricos diversos.  
NOTAS\_CODIFICACAO: Coluna mantida conforme solicitado. A natureza exata desta pontuação não foi especificada na consulta, mas é tratada como um dado numérico.

---

ID\_ORIGINAL\_QUESTAO: Q6 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Data de Nascimento  
NOME\_VARIAVEL\_PROCESSADA(S): IDADE  
DESCRICAO\_VARIAVEL: Idade do participante em anos completos.  
TIPO\_VARIAVEL\_ORIGINAL: Data  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Inteiro)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Calculada a partir da 'Data de Nascimento' e da data da resposta mais recente no conjunto de dados (TIMESTAMP\_RESPOSTA). Idade \= anos completos.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: Datas de nascimento diversas (DD/MM/AAAA) convertidas para idade em anos.  
NOTAS\_CODIFICACAO: Se 'Data de Nascimento' original estiver ausente ou for inválida, IDADE será NaN. A data de referência para o cálculo é a data da resposta mais recente no dataset original, para garantir consistência.

---

ID\_ORIGINAL\_QUESTAO: Q3 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Mg cafeína semana  
NOME\_VARIAVEL\_PROCESSADA(S): MG\_CAFEINA\_SEMANA  
DESCRICAO\_VARIAVEL: (Calculado \- Mg cafeína semana) \- Quantidade de cafeína consumida por semana em mg.  
TIPO\_VARIAVEL\_ORIGINAL: Numérico com vírgula decimal / Texto (incluindo \#ERROR\!)  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Valores numéricos originais tiveram a vírgula decimal substituída por ponto. Convertido para tipo float.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: Valores numéricos diversos (ex: "942,6" \-\> 942.6). Respostas em branco ou "\#ERROR\!" codificadas como NaN.  
NOTAS\_CODIFICACAO: Não houve recálculo dos valores. Apenas limpeza e padronização do formato numérico conforme.1

---

ID\_ORIGINAL\_QUESTAO: Q12 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Mg cafeína dia  
NOME\_VARIAVEL\_PROCESSADA(S): MG\_CAFEINA\_DIA  
DESCRICAO\_VARIAVEL: (Calculado \- Mg cafeína dia) \- Quantidade de cafeína consumida por dia em mg.  
TIPO\_VARIAVEL\_ORIGINAL: Numérico com vírgula decimal / Texto (incluindo \#ERROR\!)  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Valores numéricos originais tiveram a vírgula decimal substituída por ponto. Convertido para tipo float.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: Valores numéricos diversos (ex: "134,66" \-\> 134.66). Respostas em branco ou "\#ERROR\!" codificadas como NaN.  
NOTAS\_CODIFICACAO: Não houve recálculo dos valores. Apenas limpeza e padronização do formato numérico conforme.1

---

ID\_ORIGINAL\_QUESTAO: Q13 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Mg homens  
NOME\_VARIAVEL\_PROCESSADA(S): MG\_HOMENS  
DESCRICAO\_VARIAVEL: (Calculado \- Mg homens) \- Quantidade de cafeína específica para homens em mg.  
TIPO\_VARIAVEL\_ORIGINAL: Numérico com vírgula decimal / Texto (incluindo \#ERROR\!)  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Valores numéricos originais tiveram a vírgula decimal substituída por ponto. Convertido para tipo float.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: Valores numéricos diversos. Respostas em branco ou "\#ERROR\!" codificadas como NaN.  
NOTAS\_CODIFICACAO: Aplicável apenas a participantes do gênero masculino. Para outros, o valor será NaN ou o valor original se presente e numérico. Não houve recálculo.

---

ID\_ORIGINAL\_QUESTAO: Q14 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Mg mulheres  
NOME\_VARIAVEL\_PROCESSADA(S): MG\_MULHERES  
DESCRICAO\_VARIAVEL: (Calculado \- Mg mulheres) \- Quantidade de cafeína específica para mulheres em mg.  
TIPO\_VARIAVEL\_ORIGINAL: Numérico com vírgula decimal / Texto (incluindo \#ERROR\!)  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Valores numéricos originais tiveram a vírgula decimal substituída por ponto. Convertido para tipo float.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: Valores numéricos diversos (ex: "412,26" \-\> 412.26). Respostas em branco ou "\#ERROR\!" (ex: participante "Venus" em 1, conforme 1\) codificadas como NaN.  
NOTAS\_CODIFICACAO: Aplicável apenas a participantes do gênero feminino. Para outros, o valor será NaN ou o valor original se presente e numérico. Não houve recálculo.

---

ID\_ORIGINAL\_QUESTAO: Q4 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Gênero  
NOME\_VARIAVEL\_PROCESSADA(S): GENERO\_COD  
DESCRICAO\_VARIAVEL: Gênero do participante.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Nominal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= 'Masculino'  
* 2 \= 'Feminino'  
* 3 \= 'Prefiro não responder'  
* 4 \= 'Não-binário'  
* NaN \= Outros valores não mapeados ou ausentes. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Masculino': 1 (Contagem: 48\)  
* 'Feminino': 2 (Contagem: 12\)  
* 'Prefiro não responder': 3 (Contagem: 3\)  
* 'Não-binário': 4 (Contagem: 3\) **NOTAS\_CODIFICACAO:** Mapeamento direto conforme consulta do usuário. Consistente com a lógica de.1 Valores ausentes representados como NaN.

---

ID\_ORIGINAL\_QUESTAO: Q7 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Em que estado você reside?  
NOME\_VARIAVEL\_PROCESSADA(S): ESTADO\_RESIDENCIA\_COD  
DESCRICAO\_VARIAVEL: Estado de residência do participante.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única / Texto livre  
TIPO\_VARIAVEL\_PROCESSADA: Nominal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Códigos numéricos únicos atribuídos a cada estado. Valores padronizados para minúsculas antes da codificação.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1, exemplo de codificação)

* 'são paulo': 1 (Contagem: 48\)  
* 'rio de janeiro': 2 (Contagem: 6\)  
* 'minas gerais': 3 (Contagem: 10\)  
* 'distrito federal': 4 (Contagem: 4\)  
* 'alagoas': 5 (Contagem: 2\)  
* 'pernambuco': 6 (Contagem: 3\)  
* 'paraná': 7 (Contagem: 2\)  
* 'bahia': 8 (Contagem: 2\)  
* 'santa catarina': 9 (Contagem: 2\)  
* 'ceará': 10 (Contagem: 1\)  
* 'paraíba': 11 (Contagem: 1\)  
* 'espirito santo': 12 (Contagem: 2\)  
* 'rio grande do sul': 13 (Contagem: 1\)  
* 'rondônia': 14 (Contagem: 1\)  
* 'sergipe': 15 (Contagem: 1\)  
* NaN \= Ausente/Branco. **NOTAS\_CODIFICACAO:** Cada estado único observado nos dados recebe um código numérico. A lista acima reflete os estados presentes em 1 e suas respectivas contagens, com códigos atribuídos sequencialmente após padronização.

---

ID\_ORIGINAL\_QUESTAO: Q8 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Em qual cidade você reside?  
NOME\_VARIAVEL\_PROCESSADA(S): CIDADE\_RESIDENCIA\_PREENCHIDO  
DESCRICAO\_VARIAVEL: Indica se a cidade de residência foi informada.  
TIPO\_VARIAVEL\_ORIGINAL: Texto livre  
TIPO\_VARIAVEL\_PROCESSADA: Binária  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= Cidade informada (campo não vazio)  
* 0 \= Cidade não informada (campo vazio ou apenas espaços) **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** Diversas cidades. **NOTAS\_CODIFICACAO:** Dada a alta variabilidade e a instrução da consulta para tabulação inicial, esta coluna foi codificada para indicar apenas a presença (1) ou ausência (0) de uma resposta. Uma codificação detalhada por cidade não foi realizada. 1 sugere uma abordagem similar de codificação binária (informada/não informada) como simplificação.

---

ID\_ORIGINAL\_QUESTAO: Q9 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Nível de educação  
NOME\_VARIAVEL\_PROCESSADA(S): NIVEL\_EDUC\_COD  
DESCRICAO\_VARIAVEL: Nível de educação do participante.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Ordinal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: (Baseado nos valores de 1 e na ordem da consulta)

* 1 \= 'Ensino médio completo'  
* 2 \= 'Ensino superior incompleto'  
* 3 \= 'Ensino superior completo'  
* 4 \= 'Pós-graduação'  
* NaN \= Outros valores não mapeados ou ausentes. (A categoria 'Ensino médio incompleto' da consulta não foi observada em 1). **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Ensino médio completo': 1 (Contagem: 12\)  
* 'Ensino superior incompleto': 2 (Contagem: 37\)  
* 'Ensino superior completo': 3 (Contagem: 2\)  
* 'Pós-graduação': 4 (Contagem: 17\) **NOTAS\_CODIFICACAO:** Códigos atribuídos para refletir a progressão educacional. A codificação inicia com o nível mais baixo observado nos dados ('Ensino médio completo').

---

ID\_ORIGINAL\_QUESTAO: Q10 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Ocupação profissional  
NOME\_VARIAVEL\_PROCESSADA(S): OCUPACAO\_COD  
DESCRICAO\_VARIAVEL: Ocupação profissional do participante.  
TIPO\_VARIAVEL\_ORIGINAL: Texto livre  
TIPO\_VARIAVEL\_PROCESSADA: Nominal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: As respostas foram padronizadas (minúsculas, remoção de espaços) e codificadas conforme a lista de 1, com ajustes baseados nas frequências de.1 Respostas menos frequentes ou muito variadas são agrupadas em "Outra\_Ocupacao" (código 99).  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Exemplos baseados em 1 e 1, lista completa extensa no arquivo de dados e conforme 1\)

* 'estudante': 1 (Inclui "Estudante", "estudante", "Estudante universitária", "Estudante de mestrado", "Estudante de Pós graduação", "Mestrando", "Doutorando", "Aluna de doutorado", "bolsista", "Pesquisador de posgraduação") (Contagem agregada de 1 para 'Estudante' e variações: 22 \+ 1 \+ 1 \+ 1 \+ 1 \+ 1 \+ 1 \+ 1 \+ 1 \= 30\)  
* 'psicólogo': 4 (Inclui "Psicólogo", "Psicóloga") (Contagem agregada: 2 \+ 1 \= 3\)  
* 'designer gráfico': 14 (Inclui "Designer Gráfico") (Contagem agregada: 2\)  
* 'professor': 31 (Inclui "Professor", "Professor \- bolsista", "Professora") (Contagem agregada: 2 \+ 1 \+ 1 \= 4\)  
* ... (outras ocupações conforme 1 e 1)  
* 'outra ocupacao': 99  
* NaN \= Não informado/Branco. **NOTAS\_CODIFICACAO:** Devido à grande variedade, o esquema de codificação de 1 foi primariamente utilizado. Ocupações em 1 foram mapeadas para esses códigos ou para o código 99 ('Outra Ocupação') se não correspondessem diretamente e fossem infrequentes. A padronização (ex: "Estudante" e "estudante" para o mesmo código) foi aplicada. A alta cardinalidade desta variável torna o agrupamento essencial para análises significativas.

---

ID\_ORIGINAL\_QUESTAO: Q11 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Em qual nível você se classifica como jogador de esportes eletrônicos?  
NOME\_VARIAVEL\_PROCESSADA(S): NIVEL\_JOGADOR\_COD  
DESCRICAO\_VARIAVEL: Autoclassificação do nível como jogador de e-sports.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Ordinal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= 'Amador/Jogador casual'  
* 2 \= 'Semi-Profissional'  
* 3 \= 'Profissional'  
* NaN \= Outros valores não mapeados ou ausentes. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Amador/Jogador casual': 1 (Contagem: 50\)  
* 'Semi-Profissional': 2 (Contagem: 15\)  
* 'Profissional': 3 (Contagem: 2\) **NOTAS\_CODIFICACAO:** Códigos refletem uma progressão no nível de habilidade/comprometimento. Mapeamento direto conforme consulta.

---

ID\_ORIGINAL\_QUESTAO: Q15 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: "Quantas horas por dia, em média, você joga e-sports?"  
NOME\_VARIAVEL\_PROCESSADA(S): HORAS\_JOGO\_PRINCIPAL\_MEDIA\_DIA  
DESCRICAO\_VARIAVEL: Horas por dia, em média, dedicadas ao jogo de e-sports principal.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float) / Ordinal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 'Menos de 1 hora': 0.5  
* '1-2 horas': 1.5  
* '2-4 horas': 3.0  
* '3 HORAS': 3.0 (Mapeado para a faixa '2-4 horas')  
* '4-6 horas': 5.0  
* 'Não jogo diariamente, mas qnd jogo é entre 4-6 horas': 5.0 (Interpretado como a média de horas nos dias em que joga, mapeado para a faixa '4-6 horas')  
* 'Mais de 6 horas': 7.0  
* 'Jogo somente aos finais de semana': NaN (Não representa uma média diária consistente para esta variável numérica)  
* 'Não jogo todo dia atualmente': NaN (Não representa uma média diária consistente)  
* 'Costumava jogar 8 horas por dia quando a grade horária da faculdade não era tão pesada, Hoje, com sorte, jogo 40 minutos por dia': 0.67 (Convertido de 40 minutos/dia)  
* 'xx': NaN  
* Valores em branco/ausentes: NaN **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1 e 1)  
* '1-2 horas': 1.5 (Contagem: 29\)  
* '2-4 horas': 3.0 (Contagem: 23\)  
* 'Mais de 6 horas': 7.0 (Contagem: 8\)  
* '4-6 horas': 5.0 (Contagem: 7\)  
* 'Menos de 1 hora': 0.5 (Contagem: 7\)  
* 'Jogo somente aos finais de semana': NaN (Contagem: 1\)  
* 'Não jogo todo dia atualmente': NaN (Contagem: 1\)  
* 'Costumava jogar 8 horas por dia quando a grade horária da faculdade não era tão pesada, Hoje, com sorte, jogo 40 minutos por dia': 0.67 (Contagem: 1\)  
* 'Não jogo diariamente, mas qnd jogo é entre 4-6 horas': 5.0 (Contagem: 1\)  
* '3 HORAS': 3.0 (Contagem: 1\)  
* 'xx': NaN (Contagem: 1\) **NOTAS\_CODIFICACAO:** Esta é a primeira ocorrência da pergunta sobre horas de jogo, presumivelmente referindo-se ao jogo principal. Respostas textuais que não puderam ser convertidas em uma média diária foram codificadas como NaN. A escolha de 7.0 para 'Mais de 6 horas' segue a sugestão da consulta. A conversão de "40 minutos" para 0.67 horas (40/60) foi aplicada.

---

ID\_ORIGINAL\_QUESTAO: Q16 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Você compete ou já competiu em campeonatos de esportes eletrônicos?  
NOME\_VARIAVEL\_PROCESSADA(S): COMPETIU\_CAMPEONATOS\_BIN  
DESCRICAO\_VARIAVEL: Participação em campeonatos de e-sports.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Binária  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= 'Sim'  
* 0 \= 'Não'  
* NaN \= Ausente/Branco. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Sim': 1  
* 'Não': 0 **NOTAS\_CODIFICACAO:** Mapeamento direto.

---

ID\_ORIGINAL\_QUESTAO: Q17 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Em qual plataforma você mais joga?  
NOME\_VARIAVEL\_PROCESSADA(S): PLATAFORMA\_PRINCIPAL\_COD  
DESCRICAO\_VARIAVEL: Plataforma principal de jogo.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Nominal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= 'PC'  
* 2 \= 'PlayStation'  
* 3 \= 'Mobile/Celular'  
* 4 \= 'Xbox'  
* NaN \= Ausente/Branco. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'PC': 1 (Contagem: 49\)  
* 'Mobile/Celular': 2 (Contagem: 9\) (Ajuste no código para manter consistência sequencial)  
* 'PlayStation': 3 (Contagem: 8\)  
* 'Xbox': 4 (Contagem: 3\) **NOTAS\_CODIFICACAO:** Mapeamento direto das categorias para códigos numéricos. Os códigos foram reordenados com base na frequência para fins de exemplo, mas no processamento final serão atribuídos conforme aparecem ou de forma alfabética, e documentados.

---

ID\_ORIGINAL\_QUESTAO: Q18 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: "Além da sua plataforma principal ( \_\_\_ ), Você joga em outra?"  
NOME\_VARIAVEL\_PROCESSADA(S): PLATAFORMA\_OUTRA\_PC\_BIN, PLATAFORMA\_OUTRA\_PLAYSTATION\_BIN, PLATAFORMA\_OUTRA\_XBOX\_BIN, PLATAFORMA\_OUTRA\_NINTENDO\_BIN, PLATAFORMA\_OUTRA\_MOBILECELULAR\_BIN, PLATAFORMA\_OUTRA\_CONSOLEANTIGO\_BIN, PLATAFORMA\_OUTRA\_OCULUS\_BIN, PLATAFORMA\_OUTRA\_NAO\_BIN  
DESCRICAO\_VARIAVEL: Indica se o participante joga em outras plataformas além da principal, com dummies para cada plataforma mencionada.  
TIPO\_VARIAVEL\_ORIGINAL: Múltipla escolha (implícito) / Texto livre  
TIPO\_VARIAVEL\_PROCESSADA: Binária (para cada plataforma)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Para cada variável PLATAFORMA\_OUTRA\_X\_BIN: 1 \= Sim (se a plataforma X foi mencionada), 0 \= Não (se não mencionada). Se a célula original estiver em branco, todas as dummies correspondentes serão NaN. Se a resposta for explicitamente "Não", PLATAFORMA\_OUTRA\_NAO\_BIN \= 1 e as demais 0\.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1 e 1\)

* Opções identificadas: 'PC', 'PlayStation', 'Xbox', 'Nintendo', 'Mobile/Celular', 'Consoles antigos', 'Oculus', 'Não'.  
* Exemplo: Resposta "PC, PlayStation" \-\> PLATAFORMA\_OUTRA\_PC\_BIN=1, PLATAFORMA\_OUTRA\_PLAYSTATION\_BIN=1, demais \= 0\. **NOTAS\_CODIFICACAO:** Transformado em múltiplas variáveis dummy. A resposta "Não" é tratada como uma categoria específica na dummy PLATAFORMA\_OUTRA\_NAO\_BIN. Opções como "Consoles antigos, também" foram padronizadas para "Consoles antigos".

---

ID\_ORIGINAL\_QUESTAO: Q19 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Qual é o seu jogo eletrônico principal?  
NOME\_VARIAVEL\_PROCESSADA(S): JOGO\_PRINCIPAL\_COD  
DESCRICAO\_VARIAVEL: Jogo eletrônico principal do participante.  
TIPO\_VARIAVEL\_ORIGINAL: Texto livre  
TIPO\_VARIAVEL\_PROCESSADA: Nominal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Jogos mais frequentes (de 1, guiados por 1\) recebem códigos únicos. Outros são agrupados em Outro\_Jogo\_Principal (código 99). Nomes padronizados (ex: "Counter-Strike: Global Offensive" e "Counter-Strike" agrupados se apropriado).  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Exemplos baseados em 1 e 1\)

* 'League of Legends': 1 (Contagem: 24\)  
* 'VALORANT': 2 (Contagem: 12\)  
* 'Counter-Strike' (incluindo 'Counter-Strike: Global Offensive'): 3 (Contagem: 8 \+ 1 \= 9\)  
* 'FIFA, EA FC ou PES': 4 (Contagem: 5\)  
* 'Fortnite': 5 (Contagem: 4\)  
* 'Call of Duty: Warzone': 6 (Contagem: 3\)  
* ... (outros jogos conforme 1 e frequências de 1)  
* 'Outro\_Jogo\_Principal': 99  
* NaN \= Não informado/Branco. **NOTAS\_CODIFICACAO:** Alta cardinalidade. Agrupamento e categorização são necessários. A lista de 1 é uma referência primária, ajustada com dados de.1

---

ID\_ORIGINAL\_QUESTAO: Q20 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Há quanto tempo você joga esse jogo?  
NOME\_VARIAVEL\_PROCESSADA(S): TEMPO\_JOGO\_PRINCIPAL\_COD  
DESCRICAO\_VARIAVEL: Tempo de jogo do jogo principal.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Ordinal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= 'Menos de 6 meses'  
* 2 \= 'Entre 6 meses e 1 ano'  
* 3 \= 'Entre 1 ano e 2 anos'  
* 4 \= 'Entre 2 anos e 5 anos'  
* 5 \= 'Entre 5 anos e 10 anos'  
* 6 \= 'Mais de 10 anos'  
* NaN \= Ausente/Branco. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** Conforme esquema acima, com base nas opções de.1 **NOTAS\_CODIFICACAO:** Códigos refletem a duração crescente.

---

ID\_ORIGINAL\_QUESTAO: Q21 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Qual(is) outro(s) você joga?  
NOME\_VARIAVEL\_PROCESSADA(S): Múltiplas variáveis dummy, ex: OUTROJOGO\_RAINBOWSIX\_BIN, OUTROJOGO\_FIFA\_EAFC\_PES\_BIN, OUTROJOGO\_LOL\_BIN, OUTROJOGO\_VALORANT\_BIN, OUTROJOGO\_MINECRAFT\_BIN, OUTROJOGO\_NENHUM\_BIN, OUTROJOGO\_OUTROS\_BIN.  
DESCRICAO\_VARIAVEL: Outros jogos eletrônicos jogados pelo participante.  
TIPO\_VARIAVEL\_ORIGINAL: Texto livre (múltiplas respostas separadas por vírgula)  
TIPO\_VARIAVEL\_PROCESSADA: Binária (para cada jogo/categoria)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Para cada variável OUTROJOGO\_X\_BIN: 1 \= Sim (se o jogo X foi mencionado), 0 \= Não (se não mencionado). Resposta "Nenhum" codificada em OUTROJOGO\_NENHUM\_BIN \= 1\. Jogos menos frequentes agrupados em OUTROJOGO\_OUTROS\_BIN \= 1\. Se a célula original estiver vazia, todas as dummies serão NaN.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1 e 1\)

* Opções comuns identificadas: 'Rainbow Six Siege', 'FIFA, EA FC ou PES', 'League of Legends', 'VALORANT', 'Minecraft', 'Counter-Strike: Global Offensive', 'Fortnite', 'Overwatch', 'Nenhum', etc. **NOTAS\_CODIFICACAO:** Requer a identificação dos jogos mais citados para criar as dummies. A padronização de nomes de jogos é crucial (ex: "FIFA, EA FC ou PES" tratado como uma categoria "FIFA\_EAFC\_PES").

---

ID\_ORIGINAL\_QUESTAO: Q22 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: "Quantas horas por dia, em média, você joga \\ne-sports?" (segunda ocorrência)  
NOME\_VARIAVEL\_PROCESSADA(S): HORAS\_JOGO\_OUTROS\_MEDIA\_DIA  
DESCRICAO\_VARIAVEL: Horas por dia, em média, dedicadas a outros jogos de e-sports.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float) / Ordinal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Idêntica à HORAS\_JOGO\_PRINCIPAL\_MEDIA\_DIA (Q15).

* 'Menos de 1 hora': 0.5  
* '1-2 horas': 1.5  
* '2-4 horas': 3.0  
* '3 HORAS': 3.0  
* '4-6 horas': 5.0  
* 'Não jogo diariamente, mas qnd jogo é entre 4-6 horas': 5.0  
* 'Mais de 6 horas': 7.0  
* 'Jogo somente aos finais de semana': NaN  
* 'Não jogo todo dia atualmente': NaN  
* 'Costumava jogar 8 horas por dia...': 0.67 (ou NaN se apenas informação passada)  
* Valores em branco/ausentes: NaN **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** Similar à Q15, baseado em 1 e.1 **NOTAS\_CODIFICACAO:** Segunda ocorrência da pergunta, presumivelmente referindo-se aos "outros jogos". Mesma lógica de conversão e tratamento de respostas textuais que Q15.

---

ID\_ORIGINAL\_QUESTAO: Q23 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Você faz parte de algum time ou organização de esportes eletrônicos?  
NOME\_VARIAVEL\_PROCESSADA(S): PARTE\_TIME\_ORG\_BIN, NOME\_TIME\_ORG\_PREENCHIDO\_BIN  
DESCRICAO\_VARIAVEL: Participação em time/organização de e-sports e se o nome foi fornecido.  
TIPO\_VARIAVEL\_ORIGINAL: Texto livre  
TIPO\_VARIAVEL\_PROCESSADA: Binária, Binária  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* PARTE\_TIME\_ORG\_BIN:  
  * 1 \= Resposta indica participação (ex: "Sim", nome do time, "Fazia parte", "Hoje em dia não mais...")  
  * 0 \= Resposta indica não participação (ex: "Não", "Não faço", "Não faço parte", "Nao")  
  * NaN \= Ausente/Branco.  
* NOME\_TIME\_ORG\_PREENCHIDO\_BIN:  
  * 1 \= Nome de time/organização específico fornecido (ex: "Leaner Energy", "FEARWW")  
  * 0 \= Resposta foi "Sim" genérico, "Não", ou em branco.  
  * NaN \= Ausente/Branco. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1 e 1)  
* Exemplos: 'Não faço': PARTE\_TIME\_ORG\_BIN=0, NOME\_TIME\_ORG\_PREENCHIDO\_BIN=0. 'Sim, Pilgrims E-Sports': PARTE\_TIME\_ORG\_BIN=1, NOME\_TIME\_ORG\_PREENCHIDO\_BIN=1. 'Sim': PARTE\_TIME\_ORG\_BIN=1, NOME\_TIME\_ORG\_PREENCHIDO\_BIN=0. **NOTAS\_CODIFICACAO:** A coluna original combina a resposta sim/não com o nome da organização. Duas variáveis são criadas para capturar essa nuance. Respostas como "Não nesse semestre" ou "Hoje não mais" são codificadas como 1 para PARTE\_TIME\_ORG\_BIN se implicam participação passada ou intermitente focada na pergunta "Você faz parte...", e 0 para NOME\_TIME\_ORG\_PREENCHIDO\_BIN se nenhum nome atual for fornecido.

---

ID\_ORIGINAL\_QUESTAO: Q24 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Você consome café?  
NOME\_VARIAVEL\_PROCESSADA(S): CONSUMO\_CAFE\_BIN  
DESCRICAO\_VARIAVEL: Consumo de café.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Binária  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= 'Sim'  
* 0 \= 'Não'  
* NaN \= Ausente/Branco. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Sim': 1  
* 'Não': 0 **NOTAS\_CODIFICACAO:** Mapeamento direto.

---

ID\_ORIGINAL\_QUESTAO: Q25 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Quantos dias por semana você consome café?  
NOME\_VARIAVEL\_PROCESSADA(S): CAFE\_DIAS\_SEMANA\_NUM  
DESCRICAO\_VARIAVEL: Frequência de consumo de café por semana.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 'Raramente': 0.5  
* '1-2 vezes por semana': 1.5  
* '3-4 vezes por semana': 3.5  
* '5-6 vezes por semana': 5.5  
* 'Todos os dias': 7  
* NaN \= Ausente/Branco, ou se CONSUMO\_CAFE\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Raramente': 0.5 (Contagem: 7\)  
* '1-2 vezes por semana': 1.5  
* '3-4 vezes por semana': 3.5 (Contagem: 15\)  
* '5-6 vezes por semana': 5.5 (Contagem: 9\)  
* 'Todos os dias': 7 (Contagem: 34\) **NOTAS\_CODIFICACAO:** Códigos refletem frequência numérica. Aplicável se CONSUMO\_CAFE\_BIN \= 1\. 'Nunca' não foi observado em 1, indicando que esta pergunta provavelmente só é exibida para consumidores de café.

---

ID\_ORIGINAL\_QUESTAO: Q26 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Em qual tipo de recipiente você costuma consumir seu café?  
NOME\_VARIAVEL\_PROCESSADA(S): CAFE\_RECIPIENTE\_VOL\_ML, CAFE\_RECIPIENTE\_TIPO\_COD  
DESCRICAO\_VARIAVEL: Tipo de recipiente e volume em mL para consumo de café.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: CAFE\_RECIPIENTE\_VOL\_ML: Numérico (Float); CAFE\_RECIPIENTE\_TIPO\_COD: Nominal.  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* CAFE\_RECIPIENTE\_VOL\_ML: Extrai o volume em mL da string.  
  * "Xícara pequena: 50 ml" \-\> 50  
  * "Xícara grande: 100 ml" \-\> 100  
  * "Caneca média: 300 ml" \-\> 300  
  * "Copo americano: 200 ml" \-\> 200  
  * "Garrafa pequena: 500 ml" \-\> 500  
  * "Cápsula (Café preparado usando máquinas que funcionam com cápsulas pré-preparadas)" \-\> NaN  
* CAFE\_RECIPIENTE\_TIPO\_COD: Código nominal para cada tipo de recipiente.  
  * 1 \= 'Xícara pequena: 50 ml'  
  * 2 \= 'Xícara grande: 100 ml'  
  * 3 \= 'Caneca média: 300 ml'  
  * 4 \= 'Copo americano: 200 ml'  
  * 5 \= 'Garrafa pequena: 500 ml'  
  * 6 \= 'Cápsula (Café preparado usando máquinas que funcionam com cápsulas pré-preparadas)'  
  * NaN \= Ausente/Branco, ou se CONSUMO\_CAFE\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1 e 1)  
* 'Xícara pequena: 50 ml': VOL\_ML=50, TIPO\_COD=1 (Contagem: 6\)  
* 'Xícara grande: 100 ml': VOL\_ML=100, TIPO\_COD=2 (Contagem: 29\)  
* 'Caneca média: 300 ml': VOL\_ML=300, TIPO\_COD=3 (Contagem: 20\)  
* 'Copo americano: 200 ml': VOL\_ML=200, TIPO\_COD=4 (Contagem: 11\)  
* 'Garrafa pequena: 500 ml': VOL\_ML=500, TIPO\_COD=5 (Contagem: 2\)  
* 'Cápsula (...)': VOL\_ML=NaN, TIPO\_COD=6 **NOTAS\_CODIFICACAO:** Duas variáveis criadas: uma para o volume numérico e outra para o código nominal do tipo de recipiente. A opção "Cápsula" não tem volume associado. Aplicável se CONSUMO\_CAFE\_BIN \= 1\.

---

ID\_ORIGINAL\_QUESTAO: Q27 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: "Com base no recipiente que você selecionou anteriormente ( \_\_\_ ""), quantas vezes no dia você consome café nesse recipiente?"  
NOME\_VARIAVEL\_PROCESSADA(S): CAFE\_VEZES\_DIA\_NUM  
DESCRICAO\_VARIAVEL: Número de vezes ao dia que consome café no recipiente selecionado.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Integer)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* '1 vez ao dia': 1  
* '2 vezes ao dia': 2  
* '3 vezes ao dia': 3  
* '4 vezes ao dia': 4  
* '5 vezes ou mais ao dia': 5  
* NaN \= Ausente/Branco, ou se CONSUMO\_CAFE\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* '1 vez ao dia': 1 (Contagem: 32\)  
* '2 vezes ao dia': 2 (Contagem: 20\)  
* '3 vezes ao dia': 3 (Contagem: 8\)  
* '4 vezes ao dia': 4 (Contagem: 3\)  
* '5 vezes ou mais ao dia': 5 (Contagem: 4\) **NOTAS\_CODIFICACAO:** Extração do número da string. Aplicável se CONSUMO\_CAFE\_BIN \= 1\.

---

ID\_ORIGINAL\_QUESTAO: Q28 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Qual tipo de café você mais costuma consumir?  
NOME\_VARIAVEL\_PROCESSADA(S): CAFE\_TIPO\_PRINCIPAL\_COD  
DESCRICAO\_VARIAVEL: Tipo de café mais consumido.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Nominal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Mapeamento de cada tipo para um código numérico. Respostas padronizadas (ex: remoção de descrições em parênteses se não essenciais para distinguir).  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1 e 1\)

* 'Coado (Café filtrado através de um coador de papel ou pano)': 1 (Contagem: 38\)  
* 'Cápsula (Café preparado usando máquinas que funcionam com cápsulas pré-preparadas)': 2 (Contagem: 5\)  
* 'Expresso (Café forte e concentrado, feito sob alta pressão)': 3 (Contagem: 5\)  
* 'Instantâneo (Café em pó que dissolve em água quente)': 4 (Contagem: 5\)  
* 'Prensa Francesa (Método em que o café é imerso em água e depois separado usando um filtro de pressão)': 5 (Contagem: 3\)  
* 'Café cremoso': 6 (Contagem: 1\)  
* 'Latte': 7 (Contagem: 1\)  
* 'Affogato': 8 (Contagem: 1\)  
* 'Cappuccino': 9 (Contagem: 1\)  
* '1 coado e 1 de cápsula por dia': 10 (Contagem: 1, se esta resposta específica de 1 estiver presente)  
* Outros tipos únicos de 1 receberão códigos sequenciais.  
* NaN \= Ausente/Branco, ou se CONSUMO\_CAFE\_BIN \= 0\. **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_CAFE\_BIN \= 1\. A resposta "1 coado e 1 de cápsula por dia" é tratada como uma categoria distinta.

---

ID\_ORIGINAL\_QUESTAO: Q29 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: "Além do tipo de café selecionado anteriormente, você costuma consumir outro tipo no mesmo dia ou tem a frequência de alternar ao longo dos dias?"  
NOME\_VARIAVEL\_PROCESSADA(S): CAFE\_CONSUMO\_OUTRO\_TIPO\_COD  
DESCRICAO\_VARIAVEL: Frequência de consumo de outros tipos de café.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Nominal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: (Baseado em 1\)

* 1 \= 'Alterno entre os dias (um dia tomo um tipo, outro dia tomo outro)'  
* 2 \= 'Geralmente consumo o mesmo tipo de café' (inclui variações com vírgula no final)  
* 3 \= 'Tomo mais de 1 tipo de café por dia'  
* 4 \= '1 coado e 1 de cápsula por dia' (se esta resposta aparecer aqui)  
* NaN \= Ausente/Branco, ou se CONSUMO\_CAFE\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** Conforme esquema acima, com base nas opções de.1 **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_CAFE\_BIN \= 1\. Padronização de respostas como 'Geralmente consumo o mesmo tipo de café,' é importante.

---

ID\_ORIGINAL\_QUESTAO: Q30 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Qual outro tipo de café você costuma consumir?  
NOME\_VARIAVEL\_PROCESSADA(S): Múltiplas variáveis dummy, ex: CAFE\_OUTRO\_INSTANTANEO\_BIN, CAFE\_OUTRO\_CAPSULA\_BIN, CAFE\_OUTRO\_EXPRESSO\_BIN, CAFE\_OUTRO\_FRAPPUCCINO\_BIN, CAFE\_OUTRO\_COADO\_BIN, CAFE\_OUTRO\_DESCAFEINADO\_BIN, CAFE\_OUTRO\_PRENSAFRANCESA\_BIN, CAFE\_OUTRO\_REFRIGERANTESENERGETICOS\_BIN, CAFE\_OUTRO\_MOCCA\_BIN.  
DESCRICAO\_VARIAVEL: Outros tipos de café consumidos.  
TIPO\_VARIAVEL\_ORIGINAL: Texto livre (múltipla escolha implícita)  
TIPO\_VARIAVEL\_PROCESSADA: Binária (para cada tipo de café)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Para cada variável CAFE\_OUTRO\_X\_BIN: 1 \= Sim (se o tipo X foi mencionado), 0 \= Não (se não mencionado). Se a célula original estiver vazia, todas as dummies serão NaN.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1\)

* Opções identificadas: 'Instantâneo (Café em pó que dissolve em água quente)', 'Cápsula (Café preparado usando máquinas que funcionam com cápsulas pré-preparadas)', 'Expresso (Café forte e concentrado, feito sob alta pressão)', 'Frappuccino (Bebida gelada à base de café, com chantilly)', 'Coado (Café filtrado através de um coador de papel ou pano)', 'Descafeinado (Café sem cafeina)', 'Prensa Francesa (...)', 'Refrigerantes e energéticos', 'Mocca'. **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_CAFE\_BIN \= 1 e CAFE\_CONSUMO\_OUTRO\_TIPO\_COD indicar consumo de outros tipos. A resposta "Refrigerantes e energéticos" é peculiar e será mantida como uma categoria dummy distinta se presente.

---

ID\_ORIGINAL\_QUESTAO: Q31 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Em quais momentos do dia você costuma consumir café?  
NOME\_VARIAVEL\_PROCESSADA(S): CAFE\_MOMENTO\_AO\_ACORDAR\_BIN, CAFE\_MOMENTO\_NO\_CAFE\_DA\_MANHA\_BIN, CAFE\_MOMENTO\_MEIO\_DA\_MANHA\_BIN, CAFE\_MOMENTO\_ANTES\_DO\_ALMOCO\_BIN, CAFE\_MOMENTO\_APOS\_ALMOCO\_BIN, CAFE\_MOMENTO\_MEIO\_DA\_TARDE\_BIN, CAFE\_MOMENTO\_NO\_JANTAR\_BIN, CAFE\_MOMENTO\_ANTES\_DE\_DORMIR\_BIN, CAFE\_MOMENTO\_DE\_MADRUGADA\_BIN, CAFE\_MOMENTO\_DURANTE\_SESSOES\_JOGOS\_TREINOS\_BIN, CAFE\_MOMENTO\_AS\_VEZES\_HORARIO\_ALTERNADO\_BIN, CAFE\_MOMENTO\_QUANDO\_PRECISO\_CONCENTRAR\_BIN. (Nomes baseados nas opções de 1 e 1, padronizados).  
DESCRICAO\_VARIAVEL: Momentos do dia em que o café é consumido.  
TIPO\_VARIAVEL\_ORIGINAL: Múltipla escolha (texto com vírgulas)  
TIPO\_VARIAVEL\_PROCESSADA: Binária (para cada momento)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Para cada variável CAFE\_MOMENTO\_X\_BIN: 1 \= Sim (se o momento X foi mencionado), 0 \= Não (se não mencionado). Se a célula original estiver vazia, todas as dummies serão NaN.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1 e 1\)

* Opções padronizadas identificadas: 'ao acordar', 'no café da manhã', 'meio da manhã (por volta das 10h-11h)', 'antes do almoço', 'após o almoço', 'meio da tarde (por volta das 15h-16h)', 'no jantar', 'antes de dormir', 'de madrugada (entre 22h-04h)', 'durante sessões de jogos ou treinos', 'as vezes durante o dia, em horário alternado', 'quando preciso de concentrar para um projeto'. **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_CAFE\_BIN \= 1\. Cada momento único se torna uma variável dummy.

---

ID\_ORIGINAL\_QUESTAO: Q32 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Você consome energéticos?  
NOME\_VARIAVEL\_PROCESSADA(S): CONSUMO\_ENERGETICOS\_BIN  
DESCRICAO\_VARIAVEL: Consumo de energéticos.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Binária  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= 'Sim'  
* 0 \= 'Não'  
* NaN \= Ausente/Branco. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Sim': 1  
* 'Não': 0 **NOTAS\_CODIFICACAO:** Mapeamento direto.

---

ID\_ORIGINAL\_QUESTAO: Q33 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Quantos dias por semana você consome energético?  
NOME\_VARIAVEL\_PROCESSADA(S): ENERGETICO\_DIAS\_SEMANA\_NUM  
DESCRICAO\_VARIAVEL: Frequência de consumo de energético por semana.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 'Raramente': 0.5  
* '1-2 vezes por semana': 1.5  
* '3-4 vezes por semana': 3.5  
* '5-6 vezes por semana': 5.5  
* 'Todos os dias': 7  
* 'Nunca': 0 (Se explicitamente respondido)  
* NaN \= Ausente/Branco, ou se CONSUMO\_ENERGETICOS\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Raramente': 0.5  
* '1-2 vezes por semana': 1.5  
* '3-4 vezes por semana': 3.5  
* '5-6 vezes por semana': 5.5  
* 'Todos os dias': 7  
* 'Nunca': 0 **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_ENERGETICOS\_BIN \= 1\.

---

ID\_ORIGINAL\_QUESTAO: Q34 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Qual tipo de energético você mais costuma consumir?  
NOME\_VARIAVEL\_PROCESSADA(S): ENERGETICO\_TIPO\_PRINCIPAL\_COD  
DESCRICAO\_VARIAVEL: Tipo de energético mais consumido.  
TIPO\_VARIAVEL\_ORIGINAL: Texto livre  
TIPO\_VARIAVEL\_PROCESSADA: Nominal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Mapeamento de cada tipo para um código numérico. Respostas padronizadas.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1 e 1\)

* 'Monster': 1 (Contagem: 25\)  
* 'Red Bull': 2 (Contagem: 15\)  
* 'TNT' (inclui "TNT tradicional", "TNT pêssego"): 3 (Contagem: 2\)  
* 'Baly': 4 (Contagem: 2\)  
* 'Flying Horse': 5 (Contagem: 1\)  
* 'Flash Power': 6 (Contagem: 1\)  
* 'Tsunami': 7 (Contagem: 1\)  
* 'Fusion': 8 (Conforme 1)  
* "Mais genericos, como ": 9 (Conforme 1, codificado como "Genéricos")  
* Outros tipos únicos de 1 receberão códigos sequenciais.  
* NaN \= Ausente/Branco, ou se CONSUMO\_ENERGETICOS\_BIN \= 0\. **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_ENERGETICOS\_BIN \= 1\. Respostas como "os de 2L \- marcas diversas" são agrupadas em "Genéricos" ou "Outro".

---

ID\_ORIGINAL\_QUESTAO: Q35 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Qual o tamanho da lata ou recipiente do \_\_\_ que você costuma consumir? (Energético)  
NOME\_VARIAVEL\_PROCESSADA(S): ENERGETICO\_TAMANHO\_RECIPIENTE\_COD, ENERGETICO\_TAMANHO\_RECIPIENTE\_ML\_NUM  
DESCRICAO\_VARIAVEL: Tamanho do recipiente de energético e volume em mL.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: ENERGETICO\_TAMANHO\_RECIPIENTE\_COD: Nominal; ENERGETICO\_TAMANHO\_RECIPIENTE\_ML\_NUM: Numérico (Float).  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* ENERGETICO\_TAMANHO\_RECIPIENTE\_ML\_NUM: Extrai o volume em mL.  
  * "Pequeno (aprox, 250ml)" \-\> 250  
  * "Médio (aprox, 355ml)" \-\> 355  
  * "Grande (aprox, 473ml)" \-\> 473  
  * "Copos de 200ml durante o dia nos finais de semana apenas" \-\> 200 (ou NaN se a interpretação for muito complexa para um valor único de recipiente)  
* ENERGETICO\_TAMANHO\_RECIPIENTE\_COD:  
  * 1 \= 'Pequeno (aprox, 250ml)'  
  * 2 \= 'Médio (aprox, 355ml)'  
  * 3 \= 'Grande (aprox, 473ml)'  
  * 4 \= 'Copos de 200ml durante o dia nos finais de semana apenas'  
  * NaN \= Ausente/Branco, ou se CONSUMO\_ENERGETICOS\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1 e 1)  
* 'Grande (aprox, 473ml)': ML\_NUM=473, COD=3 (Contagem: 25\)  
* 'Médio (aprox, 355ml)': ML\_NUM=355, COD=2 (Contagem: 12\)  
* 'Pequeno (aprox, 250ml)': ML\_NUM=250, COD=1 (Contagem: 5\)  
* 'Copos de 200ml...': ML\_NUM=200, COD=4 (se presente) **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_ENERGETICOS\_BIN \= 1\. A resposta "Copos de 200ml..." é específica; o volume 200 é extraído.

---

ID\_ORIGINAL\_QUESTAO: Q36 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: "No dia que você costuma consumir energético, quantas vezes você toma essa porção \_\_\_?"  
NOME\_VARIAVEL\_PROCESSADA(S): ENERGETICO\_VEZES\_DIA\_NUM  
DESCRICAO\_VARIAVEL: Número de vezes ao dia que consome a porção de energético.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Integer)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* '1 vez ao dia': 1  
* '2 vezes ao dia': 2  
* '3 vezes ao dia': 3  
* '5 vezes ou mais ao dia': 5  
* NaN \= Ausente/Branco, ou se CONSUMO\_ENERGETICOS\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* '1 vez ao dia': 1 (Contagem: 35\)  
* '2 vezes ao dia': 2 (Contagem: 5\)  
* '3 vezes ao dia': 3 (Contagem: 1\)  
* '5 vezes ou mais ao dia': 5 (Contagem: 1\) **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_ENERGETICOS\_BIN \= 1\.

---

ID\_ORIGINAL\_QUESTAO: Q37 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Em quais momentos do dia você costuma consumir energético?  
NOME\_VARIAVEL\_PROCESSADA(S): ENERGETICO\_MOMENTO\_DURANTE\_SESSOES\_JOGOS\_TREINOS\_BIN, ENERGETICO\_MOMENTO\_MEIO\_DA\_MANHA\_BIN, ENERGETICO\_MOMENTO\_MEIO\_DA\_TARDE\_BIN, ENERGETICO\_MOMENTO\_AO\_ACORDAR\_BIN, ENERGETICO\_MOMENTO\_NO\_CAFE\_DA\_MANHA\_BIN, ENERGETICO\_MOMENTO\_NA\_MADRUGADA\_BIN, ENERGETICO\_MOMENTO\_NO\_JANTAR\_BIN, ENERGETICO\_MOMENTO\_APOS\_ALMOCO\_BIN, ENERGETICO\_MOMENTO\_ANTES\_DO\_ALMOCO\_BIN, ENERGETICO\_MOMENTO\_NO\_ALMOCO\_BIN, ENERGETICO\_MOMENTO\_ANTES\_DE\_DORMIR\_BIN, ENERGETICO\_MOMENTO\_NO\_DIA\_10\_BIN, ENERGETICO\_MOMENTO\_RARAMENTE\_BIN.  
DESCRICAO\_VARIAVEL: Momentos do dia em que o energético é consumido.  
TIPO\_VARIAVEL\_ORIGINAL: Múltipla escolha (texto com vírgulas)  
TIPO\_VARIAVEL\_PROCESSADA: Binária (para cada momento)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Para cada ENERGETICO\_MOMENTO\_X\_BIN: 1 \= Sim, 0 \= Não. NaN se pergunta original ausente.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1 e 1\)

* Opções padronizadas: 'durante sessões de jogos ou treinos', 'meio da manhã (por volta das 10h-11h)', 'meio da tarde (por volta das 15h-16h)', 'ao acordar', 'no café da manhã', 'na madrugada (entre 22h-04h)', 'no jantar', 'após o almoço', 'antes do almoço', 'no almoço', 'antes de dormir', 'no dia 10', 'raramente'. **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_ENERGETICOS\_BIN \= 1\. A resposta "Raramente" é tratada como uma categoria de momento.

---

ID\_ORIGINAL\_QUESTAO: Q38 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Você consome chá?  
NOME\_VARIAVEL\_PROCESSADA(S): CONSUMO\_CHA\_BIN  
DESCRICAO\_VARIAVEL: Consumo de chá.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Binária  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 1 \= 'Sim'  
* 0 \= 'Não'  
* NaN \= Ausente/Branco. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Sim': 1  
* 'Não': 0 **NOTAS\_CODIFICACAO:** Mapeamento direto.

---

ID\_ORIGINAL\_QUESTAO: Q39 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Quantos dias por semana você consome chá?  
NOME\_VARIAVEL\_PROCESSADA(S): CHA\_DIAS\_SEMANA\_NUM  
DESCRICAO\_VARIAVEL: Frequência de consumo de chá por semana.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Float)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* 'Raramente': 0.5  
* '1-2 vezes por semana': 1.5  
* '3-4 vezes por semana': 3.5  
* '5-6 vezes por semana': 5.5  
* 'Todos os dias': 7  
* 'Nunca': 0  
* NaN \= Ausente/Branco, ou se CONSUMO\_CHA\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* 'Raramente': 0.5  
* '1-2 vezes por semana': 1.5  
* '3-4 vezes por semana': 3.5  
* '5-6 vezes por semana': 5.5  
* 'Todos os dias': 7  
* 'Nunca': 0 **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_CHA\_BIN \= 1\.

---

ID\_ORIGINAL\_QUESTAO: Q40 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Qual tipo de chá você mais consome?  
NOME\_VARIAVEL\_PROCESSADA(S): CHA\_TIPO\_PRINCIPAL\_COD  
DESCRICAO\_VARIAVEL: Tipo de chá mais consumido.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única / Texto livre  
TIPO\_VARIAVEL\_PROCESSADA: Nominal  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Mapeamento de cada tipo para um código numérico.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1 e 1\)

* 'Chá de ervas (ex: camomila, hortelã, boldo, capim-limão, hibisco, erva-doce)': 1 (Contagem: 16\)  
* 'Chá mate': 2 (Contagem: 11\)  
* 'Chá preto': 3 (Contagem: 4\)  
* 'Chá verde': 4 (Contagem: 4\)  
* 'Chá de frutas (ex: maracujá, amora, morango,,)': 5 (Contagem: 3\)  
* 'Chá oolong': 6 (Contagem: 2\)  
* 'Chimarrão': 7 (Contagem: 1\)  
* 'Chá em garrafa do Mate Leão': 8 (Contagem: 1\)  
* NaN \= Ausente/Branco, ou se CONSUMO\_CHA\_BIN \= 0\. **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_CHA\_BIN \= 1\.

---

ID\_ORIGINAL\_QUESTAO: Q41 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Em qual tipo de recipiente você costuma consumir seu chá?  
NOME\_VARIAVEL\_PROCESSADA(S): CHA\_RECIPIENTE\_COD, CHA\_RECIPIENTE\_VOL\_ML\_NUM  
DESCRICAO\_VARIAVEL: Tipo de recipiente e volume em mL para consumo de chá.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: CHA\_RECIPIENTE\_COD: Nominal; CHA\_RECIPIENTE\_VOL\_ML\_NUM: Numérico (Float).  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* CHA\_RECIPIENTE\_VOL\_ML\_NUM: Extrai o volume em mL.  
  * "Copo americano: 200 ml" \-\> 200  
  * "Caneca média: 300 ml" \-\> 300  
  * "Xícara grande: 100 ml" \-\> 100  
  * "Garrafa pequena: 500 ml" \-\> 500  
  * "Xícara pequena: 50 ml" \-\> 50  
  * "Garrafa de 1 Litro: 1,000 ml" \-\> 1000  
  * "Garrafa de 2 Litros: 2,000 ml" \-\> 2000  
* CHA\_RECIPIENTE\_COD:  
  * 1 \= 'Copo americano: 200 ml'  
  * 2 \= 'Caneca média: 300 ml'  
  * 3 \= 'Xícara grande: 100 ml'  
  * 4 \= 'Garrafa pequena: 500 ml'  
  * 5 \= 'Xícara pequena: 50 ml'  
  * 6 \= 'Garrafa de 1 Litro: 1,000 ml'  
  * 7 \= 'Garrafa de 2 Litros: 2,000 ml'  
  * NaN \= Ausente/Branco, ou se CONSUMO\_CHA\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1 e 1)  
* 'Caneca média: 300 ml': VOL\_ML=300, COD=2 (Contagem: 19\)  
* 'Xícara grande: 100 ml': VOL\_ML=100, COD=3 (Contagem: 16\)  
* 'Copo americano: 200 ml': VOL\_ML=200, COD=1 (Contagem: 13\)  
* 'Garrafa pequena: 500 ml': VOL\_ML=500, COD=4 (Contagem: 4\)  
* 'Lata Padrão/Copo grande: 330 ml / 350 ml': VOL\_ML=350 (usando o maior valor da faixa), COD= (novo código se necessário, ou mapear para existente se apropriado) (Contagem: 1\) \- *Nota: esta opção não estava em 1 para chá, mas está em.1 Será tratada como um novo tipo ou agrupada se apropriado, e o volume extraído.*  
* 'Xícara pequena: 50 ml': VOL\_ML=50, COD=5 (Conforme 1)  
* 'Garrafa de 1 Litro: 1,000 ml': VOL\_ML=1000, COD=6 (Conforme 1)  
* 'Garrafa de 2 Litros: 2,000 ml': VOL\_ML=2000, COD=7 (Conforme 1) **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_CHA\_BIN \= 1\. A opção "Lata Padrão/Copo grande: 330 ml / 350 ml" de 1 será adicionada ao esquema de codificação.

---

ID\_ORIGINAL\_QUESTAO: Q42 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: "Com base no recipiente que você selecionou anteriormente (\_), quantas vezes ao dia você consome chá nesse recipiente?"  
NOME\_VARIAVEL\_PROCESSADA(S): CHA\_VEZES\_DIA\_NUM  
DESCRICAO\_VARIAVEL: Número de vezes ao dia que consome chá no recipiente selecionado.  
TIPO\_VARIAVEL\_ORIGINAL: Seleção única  
TIPO\_VARIAVEL\_PROCESSADA: Numérico (Integer)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO:

* '1 vez ao dia': 1  
* '2 vezes ao dia': 2  
* '3 vezes ao dia': 3  
* '4 vezes ao dia': 4  
* '5 vezes ou mais ao dia': 5  
* NaN \= Ausente/Branco, ou se CONSUMO\_CHA\_BIN \= 0\. **VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS:** (Baseado em 1)  
* '1 vez ao dia': 1 (Contagem: 34\)  
* '2 vezes ao dia': 2 (Contagem: 13\)  
* '3 vezes ao dia': 3 (Contagem: 2\)  
* '5 vezes ou mais ao dia': 5 (Contagem: 1\) **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_CHA\_BIN \= 1\.

---

ID\_ORIGINAL\_QUESTAO: Q43 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: "Além do seu chá principal (\_), você consome outro tipo de chá?"  
NOME\_VARIAVEL\_PROCESSADA(S): Múltiplas variáveis dummy, ex: CHA\_OUTRO\_VERDE\_BIN, CHA\_OUTRO\_GELADO\_BIN, CHA\_OUTRO\_GENGIBRE\_BIN, CHA\_OUTRO\_PRETO\_BIN, CHA\_OUTRO\_ERVAS\_BIN, CHA\_OUTRO\_FRUTAS\_BIN, CHA\_OUTRO\_MATE\_BIN, CHA\_OUTRO\_OOLONG\_BIN, CHA\_OUTRO\_CHIMARRAO\_BIN, CHA\_OUTRO\_BRANCO\_BIN, CHA\_OUTRO\_MATELEAOGARRAFA\_BIN. (Nomes baseados em 1 e 1).  
DESCRICAO\_VARIAVEL: Outros tipos de chá consumidos.  
TIPO\_VARIAVEL\_ORIGINAL: Texto livre (múltiplas respostas separadas por vírgula)  
TIPO\_VARIAVEL\_PROCESSADA: Binária (para cada tipo de chá)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Para cada CHA\_OUTRO\_X\_BIN: 1 \= Sim, 0 \= Não. NaN se pergunta original ausente.  
VALORES\_UNICOS\_ORIGINAIS\_E\_CODIGOS\_MAPEADOS: (Baseado em 1 e 1\)

* Opções padronizadas: 'chá verde', 'chá gelado (ice tea)', 'chá gengibre', 'chá preto', 'chá de ervas', 'chá de frutas', 'chá mate', 'chá oolong', 'chimarrão', 'chá branco', 'chá em garrafa do mate leão'. **NOTAS\_CODIFICACAO:** Aplicável se CONSUMO\_CHA\_BIN \= 1\. Cada tipo de chá único se torna uma variável dummy.

---

ID\_ORIGINAL\_QUESTAO: Q44 (Conforme 1\)  
NOME\_COLUNA\_ORIGINAL: Em quais momentos do dia você costuma consumir seu chá?  
NOME\_VARIAVEL\_PROCESSADA(S): CHA\_MOMENTO\_AO\_ACORDAR\_BIN, CHA\_MOMENTO\_NO\_CAFE\_DA\_MANHA\_BIN, CHA\_MOMENTO\_MEIO\_DA\_MANHA\_BIN, CHA\_MOMENTO\_ANTES\_DO\_ALMOCO\_BIN, CHA\_MOMENTO\_APOS\_ALMOCO\_BIN, CHA\_MOMENTO\_MEIO\_DA\_TARDE\_BIN, CHA\_MOMENTO\_NO\_JANTAR\_BIN, CHA\_MOMENTO\_ANTES\_DE\_DORMIR\_BIN, CHA\_MOMENTO\_NA\_MADRUGADA\_BIN, CHA\_MOMENTO\_DURANTE\_SESSOES\_JOGOS\_TREINOS\_BIN, CHA\_MOMENTO\_ENTRE\_CAFE\_ALMOCO\_BIN, CHA\_MOMENTO\_DURANTE\_REFEICOES\_BIN.  
DESCRICAO\_VARIAVEL: Momentos do dia em que o chá é consumido.  
TIPO\_VARIAVEL\_ORIGINAL: Múltipla escolha (texto com vírgulas)  
TIPO\_VARIAVEL\_PROCESSADA: Binária (para cada momento)  
ESQUEMA\_CODIFICACAO\_TRANSFORMACAO: Para cada \`CHA\_MOMENTO\_

#### **Referências citadas**

1. IC\_Dados\_Curados \- Worksheet (1).csv