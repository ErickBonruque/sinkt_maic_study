# Simulação SINKT — Alunos e Conceitos

**Data de Criação:** 16 de novembro de 2025  

## Visão Geral

Este projeto implementa uma simulação realista do modelo de rastreamento de conhecimento baseado em BKT (Bayesian Knowledge Tracing), conforme solicitado para demonstrar o comportamento probabilístico do aprendizado. A simulação modela a evolução do domínio de **5 alunos** (A–E) sobre **8 conceitos** (K01–K08) ao longo de **10 interações** cada.

O objetivo é calcular e visualizar a evolução da probabilidade de domínio (pᵢ) de cada aluno em cada conceito, aplicando as fórmulas de atualização do modelo BKT:

-   **Se acerto:** pᵢ₊₁ = pᵢ + α(1 − pᵢ)
-   **Se erro:** pᵢ₊₁ = pᵢ(1 − β)

Com **α = 0.3** (taxa de aprendizado) e **β = 0.1** (taxa de esquecimento).

## Estrutura do Projeto

```
sinkt_simulation/
│
├── README.md                                    # Este arquivo
├── Simulacao_SINKT_Alunos_Conceitos.xlsx       # Planilha Excel com dados e resultados
├── simulacao_sinkt.py                           # Script Python da simulação
├── analise_resultados.md                        # Análise interpretativa dos resultados
├── faq_tecnica.md                               # FAQ técnica sobre o modelo
├── notas_requisitos.md                          # Notas sobre requisitos e documentação
│
└── graficos/                                    # Pasta com visualizações
    ├── evolucao_aluno_A.png
    ├── evolucao_aluno_B.png
    ├── evolucao_aluno_C.png
    ├── evolucao_aluno_D.png
    ├── evolucao_aluno_E.png
    ├── evolucao_media_conceitos.png
    ├── heatmap_dominio_final.png
    ├── comparacao_inicial_final.png
    └── taxa_acerto_evolucao.png
```

## Arquivos Principais

### 1. Planilha Excel (`Simulacao_SINKT_Alunos_Conceitos.xlsx`)

A planilha contém múltiplas abas com dados e análises:

-   **Dados Completos:** Registro de todas as interações (440 linhas), incluindo interação, resultado, probabilidade antes e depois.
-   **Resumo por Conceito:** Estatísticas agregadas por aluno e conceito (acertos, taxa de acerto, p inicial, p final, ganho).
-   **Aluno A–E:** Matrizes de resultados (1/0) para cada aluno.
-   **Evolução p - A–E:** Matrizes de evolução de probabilidade para cada aluno.
-   **Estatísticas Gerais:** Resumo de desempenho por aluno.

### 2. Gráficos

Nove visualizações foram geradas para análise:

-   **Evolução Individual (5 gráficos):** Trajetória de pᵢ para cada aluno em todos os conceitos.
-   **Evolução Média por Conceito:** Média de pᵢ ao longo das interações para cada conceito.
-   **Heatmap de Domínio Final:** Matriz de calor mostrando o domínio final de cada aluno em cada conceito.
-   **Comparação Inicial vs Final:** Gráfico de barras comparando a probabilidade média inicial e final por aluno.
-   **Taxa de Acerto Geral:** Evolução da taxa de acerto ao longo das interações.

### 3. Documentação

-   **`analise_resultados.md`:** Interpretação detalhada dos resultados, identificando quem aprendeu mais rápido, quem teve regressão e quais conceitos foram dominados.
-   **`faq_tecnica.md`:** Perguntas e respostas sobre o funcionamento do modelo, cálculo de pᵢ e lógica probabilística.

## Resultados Principais

### Estatísticas Gerais

-   **Total de interações:** 400
-   **Taxa de acerto geral:** 51.5%
-   **Probabilidade inicial média:** 0.313
-   **Probabilidade final média:** 0.723

### Desempenho por Aluno

| Aluno | P Inicial | P Final | Ganho | Destaque |
| :--- | :--- | :--- | :--- | :--- |
| **A** | 0.270 | 0.807 | +0.537 | **Maior ganho de aprendizado** |
| **B** | 0.498 | 0.732 | +0.234 | Conhecimento prévio consolidado |
| **C** | 0.254 | 0.721 | +0.467 | Grande progresso |
| **D** | 0.394 | 0.811 | +0.417 | **Melhor desempenho final** |
| **E** | 0.148 | 0.544 | +0.396 | **Dificuldades persistentes, regressões em K04 e K06** |

### Conceitos Dominados vs. Desafiadores

-   **Dominados:** K01, K02, K03, K05, K07 (alto domínio final médio)
-   **Desafiadores:** K04, K06, K08 (baixo domínio final médio)

## Como Executar a Simulação

### Pré-requisitos

-   Python 3.11+
-   Bibliotecas: `numpy`, `pandas`, `matplotlib`, `seaborn`, `openpyxl`

### Instalação de Dependências

```bash
pip3 install numpy pandas matplotlib seaborn openpyxl
```

### Execução

```bash
cd /home/ubuntu/sinkt_simulation
python3.11 simulacao_sinkt.py
```

A execução irá:

1.  Gerar os dados de simulação (440 registros).
2.  Criar a planilha Excel com múltiplas abas.
3.  Gerar 9 visualizações na pasta `graficos/`.
4.  Exibir estatísticas gerais no terminal.

## Validação dos Resultados

Os resultados foram validados através de:

-   **Análise visual:** Todos os gráficos mostram padrões coerentes (crescimento com acertos, queda com erros).
-   **Fórmulas corretas:** As fórmulas BKT foram implementadas conforme especificado.
-   **Geração automática:** A planilha e os gráficos são gerados automaticamente pelo script.
-   **Interpretação analítica:** A análise identifica corretamente os padrões de aprendizado rápido, regressão e domínio de conceitos.

## Contato e Suporte

Para dúvidas técnicas sobre a simulação, consulte a FAQ técnica (`faq_tecnica.md`).

---

**Simulação desenvolvida por Manus AI**  
**Novembro de 2025**
