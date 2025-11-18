# Projeto MAIC — Simulação de Intervenção Pedagógica

**Data de Criação:** 16 de novembro de 2025  

## Visão Geral

Este projeto implementa uma simulação de intervenção pedagógica baseada no modelo **MAIC (Massive AI-empowered Course)**, demonstrando como sistemas multi-agentes baseados em LLMs podem ser utilizados para criar experiências de aprendizado personalizadas e adaptativas.

O projeto foi desenvolvido como continuação do estudo do modelo **SINKT**, explorando a complementaridade entre rastreamento de conhecimento (SINKT) e entrega de conteúdo interativo (MAIC).

## Estrutura do Projeto

```
maic_project/
│
├── README.md                                # Este arquivo
├── notas_maic.md                            # Notas técnicas sobre o modelo MAIC
├── simulacao_agentes_maic.md                # Simulação de intervenção com 3 agentes
├── resumo_comparativo_maic_sinkt.md         # Comparação técnica MAIC & SINKT (Markdown)
└── resumo_comparativo_maic_sinkt.pdf        # Comparação técnica MAIC & SINKT (PDF)
```

## Arquivos Principais

### 1. Notas Técnicas (`notas_maic.md`)

Documento de estudo detalhado sobre o modelo MAIC, incluindo:

-   Diferença entre MOOC e MAIC
-   Arquitetura do sistema (Teaching Side e Learning Side)
-   Descrição dos agentes de sala de aula (Classmate Agents)
-   Session Controller e Manager Agent
-   Resultados do experimento na Tsinghua University
-   Limitações e aplicações práticas

### 2. Simulação de Intervenção (`simulacao_agentes_maic.md`)

Simulação completa de uma intervenção pedagógica em um cenário real:

**Cenário:** Aluno Erick com erro repetido no conceito K04 (Estruturas de Repetição - Loops)

**Agentes Ativados:**
1.  **Tutor (Deep Thinker):** Faz perguntas socráticas para estimular reflexão
2.  **Conselho (Note Taker):** Oferece estratégia estruturada (checklist Início-Fim-Passo)
3.  **Amigo (Emotional Companion):** Fornece suporte emocional e encorajamento

**Objetivos Pedagógicos:**
-   **Dimensão Cognitiva:** Corrigir modelo mental sobre loops
-   **Dimensão Estratégica:** Equipar com ferramenta metodológica
-   **Dimensão Afetiva:** Mitigar frustração e manter motivação

**Resultados Esperados:**
-   **Curto Prazo:** Correção do erro atual, aplicação da estratégia
-   **Médio Prazo:** Aumento da taxa de acerto, evolução de p (SINKT)
-   **Longo Prazo:** Autonomia na resolução de problemas, resiliência a erros

### 3. Resumo Comparativo MAIC & SINKT (`resumo_comparativo_maic_sinkt.md` + `.pdf`)

Análise técnica comparativa entre os dois modelos, incluindo:

-   Visão geral: SINKT como diagnóstico, MAIC como ação
-   Tabela comparativa detalhada
-   Análise da complementaridade
-   Ciclo de feedback SINKT ↔ MAIC
-   Exemplos práticos de integração

**Disponível em dois formatos:**
-   **Markdown:** Para leitura no GitHub ou editores de texto
-   **PDF:** Para impressão ou apresentação formal

## O que é MAIC?

MAIC (Massive AI-empowered Course) é uma nova forma de educação online que utiliza sistemas multi-agentes baseados em LLMs para criar uma sala de aula aumentada por IA. Diferente dos MOOCs tradicionais (1 vídeo para N alunos), o MAIC oferece N agentes IA para 1 aluno, proporcionando personalização completa.

### Principais Características

-   **Custo Reduzido:** De $25,000 e 60h (MOOC) para <$2 e 30min (MAIC)
-   **Personalização:** Cada aluno tem seus próprios agentes IA com personalidades distintas
-   **Adaptabilidade:** Conteúdo dinâmico gerado em tempo real baseado nas interações
-   **Suporte Emocional:** Agentes fornecem companheirismo e encorajamento
-   **Escalabilidade:** Atende milhares de alunos simultaneamente

### Agentes de Sala de Aula

O MAIC implementa quatro tipos principais de agentes-alunos:

1.  **Class Clown:** Cria ambiente descontraído, reduz ansiedade
2.  **Deep Thinker:** Faz perguntas profundas, estimula pensamento crítico
3.  **Note Taker:** Resume e organiza informações, auxilia na retenção
4.  **Inquisitive Mind:** Faz perguntas sobre o conteúdo, promove diálogo

## Complementaridade SINKT ↔ MAIC

A integração entre SINKT e MAIC cria um sistema de tutoria inteligente completo:

-   **SINKT:** Mede e prediz o domínio do aluno (probabilidade p)
-   **MAIC:** Age com base nessa medição para personalizar o ensino

**Exemplo de Integração:**
1.  SINKT detecta que p está estagnado em 0.35 para o conceito K04
2.  SINKT alerta o Manager Agent do MAIC
3.  MAIC ativa intervenção pedagógica com 3 agentes
4.  Agentes interagem com o aluno para superar o bloqueio
5.  Aluno responde novamente, SINKT atualiza p
6.  Ciclo se repete continuamente

## Validação e Resultados

### Experimento na Tsinghua University

-   Mais de 100,000 registros de aprendizado
-   Mais de 500 estudantes voluntários
-   Dois cursos testados: TAGI e HSU

### Avaliação de Qualidade (escala 1-5)

| Métrica | Score |
| :--- | :--- |
| Tone (Tom apropriado) | 4.00 |
| Clarity (Clareza) | 4.25 |
| Supportive (Suporte) | 3.57 |
| Matching (Alinhamento) | 4.18 |
| Overall (Geral) | 4.00 |

### Feedback dos Estudantes

-   Objetivos do curso claros: 4.12/5
-   Discussão de problemas: 3.91/5
-   Exploração de novos conceitos: 4.03/5
-   Envolvimento em tarefas: 3.85/5

## Aplicações Práticas

1.  **Criação rápida de cursos:** Redução drástica de tempo e custo
2.  **Personalização em escala:** Cada aluno tem experiência única
3.  **Suporte 24/7:** Agentes IA disponíveis a qualquer momento
4.  **Detecção de dificuldades:** Intervenção imediata quando necessário
5.  **Ambiente de sala de aula simulado:** Reduz isolamento do EAD

## Próximos Passos

-   Implementação prática da integração SINKT ↔ MAIC
-   Desenvolvimento de mais tipos de agentes especializados
-   Testes em diferentes domínios de conhecimento
-   Avaliação de longo prazo dos resultados de aprendizado
-   Refinamento do Manager Agent para maior precisão

---