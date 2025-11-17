# FAQ Técnica: Modelo SINKT/BKT

**Data:** 16 de novembro de 2025

## 1. O que é o modelo SINKT?

O SINKT (Structure-Aware Inductive Knowledge Tracing) é um modelo avançado de rastreamento de conhecimento que utiliza Large Language Models (LLMs) e grafos heterogêneos para modelar o aprendizado de estudantes em sistemas de tutoria inteligente. O modelo foi apresentado em um artigo científico publicado na conferência CIKM '24.

Para esta simulação, utilizamos a lógica de atualização de probabilidade baseada no **BKT (Bayesian Knowledge Tracing)**, um modelo clássico e interpretável que serve como base conceitual para muitos sistemas de rastreamento de conhecimento.

## 2. O que é pᵢ e como ele é calculado?

**pᵢ** representa a **probabilidade de domínio** de um aluno sobre um conceito específico no momento da interação **i**. É um valor entre 0 e 1, onde:

-   **0** indica que o aluno não domina o conceito.
-   **1** indica que o aluno domina completamente o conceito.

O cálculo de **pᵢ** é atualizado dinamicamente após cada interação (tentativa de resposta), utilizando as fórmulas do modelo BKT:

-   **Se o aluno acerta (resultado = 1):**
    ```
    pᵢ₊₁ = pᵢ + α(1 − pᵢ)
    ```
    Onde **α** é a taxa de aprendizado (0.3 na simulação).

-   **Se o aluno erra (resultado = 0):**
    ```
    pᵢ₊₁ = pᵢ(1 − β)
    ```
    Onde **β** é a taxa de esquecimento (0.1 na simulação).

## 3. Por que α = 0.3 e β = 0.1?

Esses valores foram escolhidos para a simulação com base em parâmetros comuns utilizados em modelos BKT em contextos educacionais. Eles representam:

-   **α = 0.3:** Quando um aluno acerta, há uma chance de 30% de que ele tenha aprendido o conceito naquele momento (ou melhorado seu domínio). Isso significa que o aprendizado é incremental, não instantâneo.
-   **β = 0.1:** Quando um aluno erra, há uma chance de 10% de que ele tenha "esquecido" ou regredido no domínio do conceito. Isso modela a possibilidade de lapsos ou falta de consolidação.

Esses parâmetros são **ajustáveis** e podem ser calibrados com base em dados reais de desempenho de alunos para melhorar a precisão do modelo.

## 4. Como a probabilidade inicial (p₀) é definida?

Na simulação, cada aluno começou com uma probabilidade inicial média diferente, refletindo seus níveis de conhecimento prévio:

| Aluno | p₀ Médio | Interpretação |
| :--- | :--- | :--- |
| A | 0.30 | Conhecimento médio |
| B | 0.50 | Conhecimento prévio bom |
| C | 0.20 | Dificuldades iniciais |
| D | 0.40 | Conhecimento bom |
| E | 0.15 | Muitas dificuldades |

Para cada conceito, a probabilidade inicial foi ligeiramente variada (±0.1) para adicionar realismo. Em um sistema real, **p₀** poderia ser estimado com base em:

-   Desempenho em um teste diagnóstico inicial.
-   Desempenho em conceitos pré-requisito.
-   Um valor padrão (ex: 0.2 ou 0.3) para novos conceitos.

## 5. Como o modelo lida com múltiplos conceitos?

O modelo mantém um estado de conhecimento **independente** para cada par (aluno, conceito). Isso significa que a probabilidade de domínio de um aluno sobre o conceito K01 não afeta diretamente sua probabilidade sobre o conceito K02.

No entanto, em sistemas mais avançados (como o SINKT completo), as relações entre conceitos (pré-requisitos, co-requisitos) podem ser modeladas através de grafos de conhecimento, permitindo que o domínio de um conceito influencie a estimativa de domínio de conceitos relacionados.

## 6. O que acontece quando um aluno acerta consecutivamente?

Quando um aluno acerta consecutivamente, sua probabilidade de domínio aumenta de forma assintótica em direção a 1.0, mas nunca atinge exatamente 1.0 (a menos que seja forçado). Por exemplo:

-   **Interação 1:** p = 0.3, acerto → p = 0.3 + 0.3(1 - 0.3) = 0.51
-   **Interação 2:** p = 0.51, acerto → p = 0.51 + 0.3(1 - 0.51) = 0.657
-   **Interação 3:** p = 0.657, acerto → p = 0.657 + 0.3(1 - 0.657) = 0.760

Cada acerto adiciona uma fração menor ao domínio, refletindo o conceito de **retornos decrescentes** no aprendizado.

## 7. O que acontece quando um aluno erra consecutivamente?

Quando um aluno erra consecutivamente, sua probabilidade de domínio diminui de forma exponencial, podendo chegar muito próximo de 0. Por exemplo:

-   **Interação 1:** p = 0.5, erro → p = 0.5(1 - 0.1) = 0.45
-   **Interação 2:** p = 0.45, erro → p = 0.45(1 - 0.1) = 0.405
-   **Interação 3:** p = 0.405, erro → p = 0.405(1 - 0.1) = 0.365

Isso modela a **regressão** do conhecimento, indicando que o aluno pode não ter consolidado o conceito ou estar enfrentando dificuldades persistentes.

## 8. Como o modelo pode ser usado para personalização?

O valor de **pᵢ** pode ser usado para:

-   **Recomendação de Conteúdo:** Se pᵢ < 0.5, o sistema pode recomendar materiais de revisão ou atividades mais simples. Se pᵢ > 0.8, o sistema pode sugerir desafios mais avançados.
-   **Feedback Adaptativo:** Alunos com baixo pᵢ podem receber feedback mais detalhado e explicativo, enquanto alunos com alto pᵢ podem receber feedback mais conciso.
-   **Identificação de Lacunas:** Conceitos com pᵢ consistentemente baixo indicam áreas onde o aluno precisa de suporte adicional.
-   **Predição de Desempenho:** O valor de pᵢ pode ser usado para estimar a probabilidade de um aluno acertar a próxima questão sobre aquele conceito.

## 9. Quais são as limitações do modelo BKT?

O modelo BKT, embora eficaz, possui algumas limitações:

-   **Independência de Conceitos:** Não modela naturalmente as relações entre conceitos (pré-requisitos, co-requisitos).
-   **Simplificação:** Assume que o aprendizado pode ser capturado por apenas dois parâmetros (α e β), o que pode não refletir a complexidade real do processo de aprendizado.
-   **Necessidade de Calibração:** Os parâmetros α e β precisam ser ajustados com dados reais para cada contexto educacional.

Modelos mais avançados, como o SINKT, superam essas limitações ao incorporar informações semânticas e estruturais através de LLMs e grafos de conhecimento.

## 10. Como validar se o modelo está funcionando corretamente?

A validação pode ser feita através de:

-   **Análise Visual:** Verificar se os gráficos de evolução de pᵢ fazem sentido (tendência de crescimento com acertos, queda com erros).
-   **Testes de Sanidade:** Simular cenários extremos (todos os acertos, todos os erros) e verificar se pᵢ converge para 1.0 ou 0.0, respectivamente.
-   **Comparação com Dados Reais:** Se disponíveis, comparar as predições do modelo com o desempenho real de alunos em testes subsequentes.
-   **Métricas de Avaliação:** Calcular métricas como AUC (Area Under the Curve) ou acurácia de predição para avaliar a capacidade do modelo de prever o desempenho futuro.
