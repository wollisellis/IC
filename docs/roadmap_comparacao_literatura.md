# Roadmap: Comparação do Consumo de Cafeína com Literatura

Este roadmap detalha passos para implementar comparações 'padrão-ouro' entre nossos resultados (276 mg/dia) e estudos externos.

## 1. Estruturar dados dos estudos externos
- Criar lista/dicionário com: nome do estudo, média (mean), desvio padrão (SD) e tamanho amostral (N).
  - Nosso estudo: `media` e `sd` calculados a partir dos dados brutos.
  - Soffner et al. 2023 (Alemanha): mean=276 mg/dia, sd≈desconhecido, N=817.
  - DiFrancisco-Donoghue et al. 2019 (EUA): mean=250 mg/dia, N≈200.
  - Trotter et al. 2020 (Austrália): mean=200 mg/dia, sd=100 mg, N≈150.

## 2. Estatística comparativa
- Utilizar `ttest_ind_from_stats` (Scipy) para testes t de duas amostras (Welch).
- Calcular effect size (Cohen's d) para magnitude de diferenças.

## 3. Visualização comparativa
- Gerar **forest plot** com médias e IC95% de cada estudo.
- Salvar figura em `notebooks/outputs/figura_comparacao_consumo.png`.

## 4. Integração na pipeline de análise
- Em `notebooks/analise_estatistica_inferencial.py`:
  1. Definir função `comparar_consumo_literatura(df, f)`.
  2. Inserir chamada a essa função em `realizar_analises()`.
  3. Escrever resultados estatísticos em `resultados_inferenciais.txt`.

## 5. Documentação no manuscrito
- Em `docs/Publicacao_Tese.md`, criar seção:
  - Tabela resumo com detales (mean ± SD, N).
  - Figura de forest plot.
  - Texto objetivo de métodos e achados.

## 6. Geração de outputs finais
- Executar scripts/notebooks para produzir arquivos:
  - `notebooks/outputs/figura_comparacao_consumo.png`
  - `docs/Publicacao_Tese_final.docx` via Pandoc.

## 7. Revisão de qualidade
- Verificar consistência de IC, p-values e effect sizes.
- Checar aderência às diretrizes de transparência (métodos, fontes de dados).

## 8. Versionamento e changelog
- Git commits claros:
  - `feat: adicionar comparação consumo vs literatura`
  - `docs: seção comparação literatura e forest plot`

## 9. Checklist final
- Métodos descritos em MATERIAIS & MÉTODOS.
- Figuras legendadas e corretas.
- Tabelas numeradas e citadas.
- Estatísticas detalhadas no Apêndice/Suplementar.

## Checklist de Implementação

- [x] 1. Estruturar dados dos estudos externos  
- [x] 2. Estatística comparativa  
- [x] 3. Visualização comparativa  
- [x] 4. Integração na pipeline de análise  
- [x] 5. Documentação no manuscrito  
- [x] 6. Geração de outputs finais  
- [x] 7. Revisão de qualidade  
- [x] 8. Versionamento e changelog  
- [x] 9. Checklist final 