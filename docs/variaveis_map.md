# Mapeamento de Variáveis: Nomes para Uso no Manuscrito vs. Nomes Técnicos no Dataset

Este arquivo serve como um glossário, associando os nomes técnicos das variáveis (conforme constam no arquivo `IC_Dados_Processados.csv` e são utilizados nos scripts de análise) aos nomes descritivos e legíveis recomendados para uso direto no texto do manuscrito (`Publicacao_Tese.md`).

| Nome Descritivo no Manuscrito                                  | Nome Técnico da Variável (no Dataset/Scripts) |
|----------------------------------------------------------------|-----------------------------------------------|
| Consumo Diário Total de Cafeína (mg)                           | `MG_CAFEINA_TOTAL_DIA`                          |
| Horas Médias de Jogo Principal por Dia                         | `HORAS_JOGO_PRINCIPAL_MEDIA_DIA`                |
| Nível de Experiência do Jogador                                | `NIVEL_JOGADOR_COD`                           |
| Ocorrência de Insônia (Sim/Não)                                | `EFEITO_ADVERSO_INSONIA_BIN`                  |
| Ocorrência de Dor de Estômago (Sim/Não)                        | `EFEITO_ADVERSO_DOR_ESTOMAGO_BIN`             |
| Ocorrência de Taquicardia (Sim/Não)                            | `EFEITO_ADVERSO_TAQUICARDIA_BIN`              |
| Ocorrência de Tremores (Sim/Não)                               | `EFEITO_ADVERSO_TREMORES_BIN`                 |
| Ocorrência de Nervosismo (Sim/Não)                             | `EFEITO_ADVERSO_NERVOSISMO_BIN`               |
| Consumo de Cafeína com Intenção de Melhorar Performance (Sim/Não) | `MELHORAR_PERFORMANCE_MOTIVO_BIN`             |
| Plataforma Principal de Jogo                                   | `PLATAFORMA_PRINCIPAL_COD`                    |
| Gênero do Participante                                         | `GENERO_COD`                                  |
| Idade do Participante (anos)                                   | `IDADE`                                       |

**Valores de Códigos para Variáveis Categóricas (Exemplos Chave):**

*   **Nível de Experiência do Jogador (`NIVEL_JOGADOR_COD`):**
    *   1: Amador/Casual
    *   2: Semi-Profissional
    *   3: Profissional
*   **Gênero do Participante (`GENERO_COD`):**
    *   1: Masculino
    *   2: Feminino
    *   3: Outro
    *   4: Prefiro Não Responder
*   **Variáveis Binárias (`_BIN`):**
    *   1: Sim (ou presença do efeito/motivo)
    *   0: Não (ou ausência do efeito/motivo)

Este mapa ajuda a manter a consistência na redação do manuscrito e a entender as referências a variáveis nos scripts e análises. 