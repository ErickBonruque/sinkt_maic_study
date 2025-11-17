# Notas sobre Requisitos - Simulação SINKT

## Documentação Analisada

### 1. SINKT Paper (CIKM '24)
- **Modelo**: Structure-Aware Inductive Knowledge Tracing with Large Language Model
- **Foco**: Knowledge Tracing (KT) para sistemas de tutoria inteligente
- **Características**:
  - Utiliza LLMs para criar grafos heterogêneos de conceitos-questões
  - Codificador de informação textual e estrutural
  - Predição de respostas de estudantes
  - Abordagem indutiva (pode prever para novos conceitos/questões)

**NOTA IMPORTANTE**: O paper SINKT não apresenta as fórmulas de atualização mencionadas no requisito (pᵢ₊₁ = pᵢ + α(1 − pᵢ) para acerto). Essas fórmulas são do modelo **BKT (Bayesian Knowledge Tracing)** clássico.

### 2. MAIC.pdf
- Ainda não analisado em detalhes

## Requisitos da Atividade

### Estrutura de Dados
- **5 alunos**: A, B, C, D, E
- **8 conceitos**: K01, K02, K03, K04, K05, K06, K07, K08
- **10 interações** por aluno (tentativas)
- Cada linha = tentativa (1 = acerto, 0 = erro)

### Fórmulas de Atualização (Modelo BKT Simplificado)
- **Se acerto**: pᵢ₊₁ = pᵢ + α(1 − pᵢ)
- **Se erro**: pᵢ₊₁ = pᵢ(1 − β)
- **Parâmetros**: α = 0.3, β = 0.1 (ajustáveis)

### Cálculos Necessários
- pᵢ inicial (probabilidade inicial de domínio)
- Evolução de pᵢ ao longo das 10 interações
- pᵢ final por conceito para cada aluno

### Visualizações
1. **Evolução individual**: Gráficos por aluno mostrando evolução de pᵢ para cada conceito
2. **Média geral**: Gráfico por conceito mostrando média de pᵢ entre todos os alunos

### Análise Interpretativa
- Identificar quem aprendeu mais rápido
- Identificar quem teve regressão
- Identificar quais conceitos foram dominados

## Esclarecimento Conceitual

O modelo SINKT do paper é um modelo avançado de deep learning que:
- Usa LLMs para representação semântica
- Emprega grafos heterogêneos para estrutura
- Utiliza GRU para modelar sequências de aprendizado
- Prediz probabilidade de resposta correta

A simulação solicitada usa **fórmulas de BKT** (modelo probabilístico clássico mais simples) para demonstrar o conceito de **evolução de domínio** (mastery/knowledge state) de forma didática e interpretável.

## Próximos Passos
1. Criar estrutura de planilha com dados simulados
2. Implementar fórmulas de atualização BKT
3. Gerar visualizações
4. Realizar análise interpretativa
5. Documentar proposta de integração
