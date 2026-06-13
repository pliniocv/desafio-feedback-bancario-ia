# Extraindo Insights de Feedbacks Bancários com IA

Projeto desenvolvido como parte do Desafio Criativo da DIO.

## Objetivo

Construir um prompt estruturado capaz de orientar uma Inteligência Artificial na análise de feedbacks de clientes bancários, transformando comentários em insights acionáveis para tomada de decisão.

## Problema

Instituições financeiras recebem milhares de feedbacks diariamente por diversos canais. Analisar essas informações manualmente é demorado e dificulta a identificação rápida de padrões, reclamações recorrentes e oportunidades de melhoria.

## Solução

Foi desenvolvido um prompt de Engenharia de Prompt que orienta a IA a:

* Classificar feedbacks por tema
* Identificar sentimento dos clientes
* Avaliar urgência e impacto
* Detectar padrões recorrentes
* Gerar recomendações estratégicas
* Produzir relatórios executivos para apoio à tomada de decisão

## Estrutura do Projeto

```text
.
├── prompt-final.md
├── banking_feedback.csv
├── generate_feedback_data.py
├── analyze_feedback.py
└── relatorio-analise.md
```

### Arquivos

| Arquivo                   | Descrição                               |
| ------------------------- | --------------------------------------- |
| prompt-final.md           | Prompt desenvolvido para o desafio      |
| banking_feedback.csv      | Base de feedbacks utilizada para testes |
| generate_feedback_data.py | Script para geração de dados simulados  |
| analyze_feedback.py       | Script de análise dos feedbacks         |
| relatorio-analise.md      | Exemplo de saída gerada                 |

## Tecnologias Utilizadas

* Engenharia de Prompt
* Inteligência Artificial Generativa
* Python
* Pandas
* Análise de Dados

## Principais Conceitos Aplicados

* Context Engineering
* Role Prompting
* Classificação de Sentimentos
* Extração de Insights
* Análise de Feedbacks
* Tomada de Decisão Orientada por Dados

## Resultado Esperado

A IA deve ser capaz de transformar feedbacks não estruturados em informações estratégicas, permitindo que equipes de Customer Experience, Produtos e Operações priorizem melhorias de forma mais eficiente.

## Autor

Plínio Ventavoli
