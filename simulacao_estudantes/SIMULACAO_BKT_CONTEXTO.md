# Simulação de Estudantes com BKT Corrigido (Bayesian Knowledge Tracing)

## Visão Geral do Projeto

Este documento descreve o processo completo de simulação de estudantes sintéticos utilizando o modelo **BKT (Bayesian Knowledge Tracing)** corrigido para o projeto SINKT. O objetivo é gerar interações realistas de estudantes respondendo questões sobre conceitos de Linux, considerando diferentes perfis cognitivos e parâmetros de aprendizagem.

**Atualização v4.0.0**: Implementadas 5 correções fundamentais baseadas em Corbett & Anderson (1995) para alinhar o modelo com o BKT clássico.

---

## 1. Perfis Cognitivos

### 1.1 Descrição dos Perfis

Foram criados **6 perfis cognitivos** distintos que representam diferentes tipos de estudantes. Cada perfil é caracterizado por 9 parâmetros fundamentais que influenciam o comportamento de aprendizagem:

#### **Parâmetros dos Perfis:**

1. **mastery_init_level** (0-1): Nível inicial de domínio do conteúdo
2. **learn_rate** (0-1): Taxa de aprendizagem (velocidade de aquisição de conhecimento)
3. **slip** (0-1): Probabilidade de erro quando o estudante sabe o conteúdo
4. **guess** (0-1): Probabilidade de acerto quando o estudante não sabe o conteúdo
5. **logic_skill** (0-1): Habilidade lógica e raciocínio algorítmico
6. **reading_skill** (0-1): Habilidade de interpretação de texto
7. **tech_familiarity** (0-1): Familiaridade com tecnologia e Linux
8. **memory_capacity** (0-1): Capacidade de retenção de memória
9. **learning_consistency** (0-1): Consistência e regularidade nos estudos

---

### 1.2 Perfis Definidos

#### **Perfil 1: Estudante Equilibrado (balanced)**
Perfil médio com habilidades balanceadas em todas as dimensões.

| Parâmetro | Valor | Peso/Influência |
|-----------|-------|-----------------|
| mastery_init_level | 0.55 | Domínio inicial moderado |
| learn_rate | 0.035 | Aprendizagem moderada |
| slip | 0.15 | Erro moderado quando sabe |
| guess | 0.15 | Acerto moderado quando não sabe |
| logic_skill | 0.55 | Habilidade lógica média |
| reading_skill | 0.55 | Interpretação média |
| tech_familiarity | 0.55 | Familiaridade média |
| memory_capacity | 0.55 | Retenção média |
| learning_consistency | 0.60 | Consistência moderada |

---

#### **Perfil 2: Aprendiz Rápido (quick_learner)**
Alta capacidade de aprendizagem e domínio inicial. Adquire conceitos rapidamente mas pode cometer erros por pressa.

| Parâmetro | Valor | Peso/Influência |
|-----------|-------|-----------------|
| mastery_init_level | 0.50 | Domínio inicial moderado |
| learn_rate | 0.08 | **Aprendizagem muito rápida** |
| slip | 0.18 | Erro elevado (pressa) |
| guess | 0.12 | Acerto baixo quando não sabe |
| logic_skill | 0.70 | **Habilidade lógica alta** |
| reading_skill | 0.65 | Interpretação boa |
| tech_familiarity | 0.80 | **Familiaridade alta** |
| memory_capacity | 0.80 | **Retenção alta** |
| learning_consistency | 0.85 | **Consistência alta** |

---

#### **Perfil 3: Estudante Cuidadoso (careful)**
Baixa taxa de erros quando sabe o conteúdo, mas aprende de forma mais gradual. Meticuloso e detalhista.

| Parâmetro | Valor | Peso/Influência |
|-----------|-------|-----------------|
| mastery_init_level | 0.45 | Domínio inicial moderado-baixo |
| learn_rate | 0.025 | Aprendizagem lenta |
| slip | 0.08 | **Erro muito baixo quando sabe** |
| guess | 0.10 | Acerto baixo quando não sabe |
| logic_skill | 0.60 | Habilidade lógica boa |
| reading_skill | 0.70 | **Interpretação alta** |
| tech_familiarity | 0.50 | Familiaridade média |
| memory_capacity | 0.70 | Retenção boa |
| learning_consistency | 0.90 | **Consistência muito alta** |

---

#### **Perfil 4: Estudante com Dificuldades (struggling)**
Baixo domínio inicial e lenta aprendizagem. Pode precisar de mais apoio e tempo para absorver conceitos.

| Parâmetro | Valor | Peso/Influência |
|-----------|-------|-----------------|
| mastery_init_level | 0.25 | **Domínio inicial baixo** |
| learn_rate | 0.015 | **Aprendizagem muito lenta** |
| slip | 0.25 | **Erro alto quando sabe** |
| guess | 0.20 | Acerto moderado quando não sabe |
| logic_skill | 0.30 | **Habilidade lógica baixa** |
| reading_skill | 0.35 | **Interpretação baixa** |
| tech_familiarity | 0.20 | **Familiaridade baixa** |
| memory_capacity | 0.40 | **Retenção baixa** |
| learning_consistency | 0.40 | **Consistência baixa** |

---

#### **Perfil 5: Pensador Lógico (logical)**
Excelente habilidade lógica mas com dificuldades em leitura. Excelente em problemas algorítmicos e matemáticos.

| Parâmetro | Valor | Peso/Influência |
|-----------|-------|-----------------|
| mastery_init_level | 0.50 | Domínio inicial moderado |
| learn_rate | 0.04 | Aprendizagem moderada |
| slip | 0.12 | Erro baixo quando sabe |
| guess | 0.08 | Acerto muito baixo quando não sabe |
| logic_skill | 0.85 | **Habilidade lógica muito alta** |
| reading_skill | 0.30 | **Interpretação baixa** |
| tech_familiarity | 0.60 | Familiaridade boa |
| memory_capacity | 0.60 | Retenção boa |
| learning_consistency | 0.75 | Consistência alta |

---

#### **Perfil 6: Estudante Intuitivo (intuitive)**
Boa intuição e habilidade de leitura, mas dificuldade com formalismo lógico. Aprende por exemplo e prática.

| Parâmetro | Valor | Peso/Influência |
|-----------|-------|-----------------|
| mastery_init_level | 0.40 | Domínio inicial moderado-baixo |
| learn_rate | 0.045 | Aprendizagem moderada-alta |
| slip | 0.16 | Erro moderado quando sabe |
| guess | 0.18 | Acerto moderado quando não sabe |
| logic_skill | 0.35 | **Habilidade lógica baixa** |
| reading_skill | 0.80 | **Interpretação muito alta** |
| tech_familiarity | 0.45 | Familiaridade moderada-baixa |
| memory_capacity | 0.65 | Retenção boa |
| learning_consistency | 0.65 | Consistência boa |

---

### 1.3 Estatísticas dos Perfis

| Parâmetro | Média | Desvio Padrão | Mínimo | Máximo |
|-----------|-------|---------------|--------|--------|
| mastery_init_level | 0.442 | 0.098 | 0.250 | 0.550 |
| learn_rate | 0.040 | 0.020 | 0.015 | 0.080 |
| slip | 0.157 | 0.052 | 0.080 | 0.250 |
| guess | 0.138 | 0.043 | 0.080 | 0.200 |
| logic_skill | 0.558 | 0.190 | 0.300 | 0.850 |
| reading_skill | 0.558 | 0.181 | 0.300 | 0.800 |
| tech_familiarity | 0.517 | 0.180 | 0.200 | 0.800 |
| memory_capacity | 0.617 | 0.125 | 0.400 | 0.800 |
| learning_consistency | 0.692 | 0.167 | 0.400 | 0.900 |

---

## 2. Geração de Estudantes Sintéticos

### 2.1 Configuração

- **Total de estudantes**: 100
- **Seed de reprodutibilidade**: 42
- **Variação individual**: ±15%

### 2.2 Distribuição por Perfil

| Perfil | Proporção | Quantidade |
|--------|-----------|------------|
| balanced | 30% | 30 estudantes |
| quick_learner | 20% | 20 estudantes |
| careful | 20% | 20 estudantes |
| struggling | 10% | 10 estudantes |
| logical | 10% | 10 estudantes |
| intuitive | 10% | 10 estudantes |

---

### 2.3 Fórmula de Geração

Cada estudante é gerado aplicando uma **variação individual aleatória** aos parâmetros do perfil base:

```
novo_valor = valor_perfil × (1 + ruído)
onde:
  ruído ~ Uniforme(-0.15, 0.15)
  novo_valor = clip(novo_valor, 0.0, 1.0)
```

**Exemplo prático:**
- Se `mastery_init_level` do perfil = 0.50
- E ruído = 0.10 (10% de aumento)
- Então: `novo_valor = 0.50 × (1 + 0.10) = 0.55`

Esta variação garante que:
1. Estudantes do mesmo perfil não sejam idênticos
2. A diversidade individual seja mantida
3. Os valores permaneçam dentro do intervalo válido [0, 1]

---

### 2.4 Estatísticas dos Estudantes Gerados

| Parâmetro | Média | Desvio Padrão | Mínimo | Máximo |
|-----------|-------|---------------|--------|--------|
| mastery_init_level | 0.469 | 0.094 | 0.231 | 0.631 |
| learn_rate | 0.041 | 0.021 | 0.013 | 0.089 |
| slip | 0.147 | 0.046 | 0.068 | 0.258 |
| guess | 0.136 | 0.037 | 0.071 | 0.229 |
| logic_skill | 0.580 | 0.169 | 0.265 | 0.962 |
| reading_skill | 0.580 | 0.156 | 0.265 | 0.907 |
| tech_familiarity | 0.549 | 0.174 | 0.175 | 0.911 |
| memory_capacity | 0.633 | 0.140 | 0.352 | 0.911 |
| learning_consistency | 0.704 | 0.168 | 0.346 | 1.000 |

---

## 3. Dados Utilizados

### 3.1 Conceitos de Linux

**Fonte**: `data/json/concepts_graph.json`

**Metadados**:
- Total de conceitos: **251**
- Total de relações: **322**
- Método de extração: Multi-Agent Council V2 (LangGraph Optimized)

**Estrutura de um conceito**:
```json
{
  "nome": "$PATH",
  "tipo": "SHELL_SCRIPT",
  "definicao": "Variável que armazena os diretórios nos quais o sistema deve buscar executáveis...",
  "capitulo_origem": "12",
  "id": "concept_000",
  "grau_entrada": 0,
  "grau_saida": 2,
  "grau_total": 2,
  "categoria": "Scripting_e_Automacao",
  "tamanho_definicao": 156,
  "nivel_detalhe": "INTERMEDIARIO",
  "quality_score": 1.0
}
```

**Exemplos de conceitos**:
1. **$PATH** (SHELL_SCRIPT): Variável que armazena diretórios de busca de executáveis
2. **\*** (SHELL_SCRIPT): Curinga para representar qualquer sequência de caracteres
3. **--help** (COMANDO): Parâmetro para obter ajuda rápida sobre comandos

**Categorias principais**:
- Scripting_e_Automacao
- Ferramentas_e_Comandos
- Sistema_de_Arquivos
- Gerenciamento_de_Processos
- Redes_e_Seguranca

---

### 3.2 Questões sobre Conceitos

**Fonte**: `data/json/questions_graph.json`

**Metadados**:
- Total de questões: **680**
- Questões por conceito (média): **2.71**

**Distribuição por tipo**:
- Multiple choice: 429 (63.1%)
- Descriptive: 251 (36.9%)

**Distribuição por dificuldade**:
- Easy: 251 (36.9%)
- Medium: 306 (45.0%)
- Hard: 123 (18.1%)

**Distribuição por nível Bloom**:
- Understand: 379 (55.7%)
- Apply: 178 (26.2%)
- Analyze: 123 (18.1%)

**Estrutura de uma questão**:
```json
{
  "id": "concept_000_q1",
  "c_id": "concept_000",
  "c_name": "$PATH",
  "c_type": "SHELL_SCRIPT",
  "type": "multiple_choice",
  "diff": "easy",
  "q": "O que é $PATH?",
  "exp": "$PATH: Variável que armazena os diretórios...",
  "rel": ["Variáveis de Ambiente", "/bin"],
  "kw": ["$path", "$path"],
  "bloom": "understand",
  "score": 2.0,
  "ans": "D",
  "opt": {
    "A": "Um comando para listar arquivos",
    "B": "Um tipo de permissão de arquivo",
    "C": "Um protocolo de rede",
    "D": "Variável que armazena os diretórios..."
  }
}
```

**Exemplos de questões**:

1. **Questão Easy (Multiple Choice)**:
   - Conceito: $PATH
   - Pergunta: "O que é $PATH?"
   - Tipo: Understand
   - Resposta: D

2. **Questão Medium (Multiple Choice)**:
   - Conceito: $PATH
   - Pergunta: "Para qual propósito é usado $PATH?"
   - Tipo: Apply
   - Resposta: A

---

## 4. Simulação de Interações com BKT

### 4.1 Configuração da Simulação

- **Interações por estudante**: 30-60 (aleatório)
- **Total de estudantes**: 100
- **Seed**: 42
- **Tipos de erro**: misconception, careless, slip, incomplete, misunderstanding
- **Versão**: 4.0.0 (com 5 correções implementadas)

---

### 4.2 As 5 Correções Implementadas

#### Correção A: Usar current_mastery na probabilidade
- **Problema anterior**: Usava `mastery_init_level` fixo, impedindo progresso de aprendizagem
- **Solução**: Função recebe `current_mastery` atualizado a cada interação
- **Impacto**: Permite curvas de aprendizagem realistas

#### Correção B: Update Bayesiano padrão
- **Problema anterior**: Update heurístico linear
- **Solução**: Implementar update Bayesiano correto:
  ```
  Se acertou: P(L|correct) = P(L)*(1-slip) / [P(L)*(1-slip) + (1-P(L))*guess]
  Se errou:   P(L|wrong)   = P(L)*slip / [P(L)*slip + (1-P(L))*(1-guess)]
  ```
- **Impacto**: Separa corretamente "saber" de "acertar por sorte"

#### Correção C: Fatores cognitivos em slip/guess
- **Problema anterior**: Fatores somados diretamente ao mastery
- **Solução**: Fatores afetam parâmetros efetivos:
  ```
  guess_eff = guess * (0.85 + 0.20*tech + 0.15*logic - 0.20*difficulty)
  slip_eff  = slip * (0.90 + 0.40*(1-consistency) + 0.20*difficulty + 0.20*(1-reading))
  ```
- **Impacto**: Modelagem mais realista de habilidades cognitivas

#### Correção D: Ruído na probabilidade final
- **Problema anterior**: Ruído aplicado ao estado interno (mastery)
- **Solução**: Ruído aplicado apenas na probabilidade observada
- **Impacto**: Mantém estado de conhecimento limpo

#### Correção E: Decay temporal ajustado
- **Problema anterior**: Decay aplicado a cada interação, muito agressivo
- **Solução**: Decay só se gap > 6h, coeficiente reduzido de 0.1 para 0.02
- **Impacto**: Decay mais realista para simulações curtas

---

### 4.3 Cálculo da Probabilidade de Resposta Correta (Corrigido)

A probabilidade é calculada usando a **fórmula BKT clássica** com parâmetros efetivos:

```python
def calculate_response_probability(current_mastery, student_params, question_difficulty):
    # Calcula parâmetros efetivos baseado em fatores cognitivos
    slip_eff, guess_eff, learn_eff = calculate_effective_params(student_params, question_difficulty)
    
    # Ajuste leve do mastery por dificuldade
    m_adj = clip(current_mastery - 0.15 * question_difficulty, 0.0, 1.0)
    
    # Fórmula BKT clássica
    prob = m_adj * (1 - slip_eff) + (1 - m_adj) * guess_eff
    
    # Ruído de consistência na probabilidade final
    if learning_consistency < 0.7:
        noise = Normal(0, (0.7 - learning_consistency) * 0.1)
        prob += noise
    
    return clip(prob, 0, 1)
```

**Componentes da fórmula**:

1. **Mastery atual**: Usa `current_mastery` (não mais o inicial)
2. **Parâmetros efetivos**: Slip e guess ajustados por fatores cognitivos
3. **Fórmula clássica**: P(correct) = P(L)*(1-slip) + (1-P(L))*guess
4. **Ruído controlado**: Apenas na observação, não no estado

---

### 4.4 Atualização do Domínio (Corrigido)

Após cada interação, o domínio é atualizado usando **update Bayesiano + transição**:

```python
def update_mastery_bkt(current_mastery, is_correct, slip, guess, learn_rate, 
                       memory_capacity, time_gap):
    # Update Bayesiano dado observação
    if is_correct:
        P_L_given_obs = P(L)*(1-slip) / [P(L)*(1-slip) + (1-P(L))*guess]
    else:
        P_L_given_obs = P(L)*slip / [P(L)*slip + (1-P(L))*(1-guess)]
    
    # Transição de aprendizagem
    P_L_next = P_L_given_obs + (1 - P_L_given_obs) * learn_rate
    
    # Decay temporal (só se gap > 6h)
    if time_gap > 6 * 3600:
        time_factor = min((time_gap - 6*3600) / 86400, 1.0)
        decay_factor = 1 - (1 - memory_capacity) * 0.02 * time_factor
        P_L_next *= max(0.5, decay_factor)
    
    return clip(P_L_next, 0, 1)
```

---

### 4.5 Estrutura de uma Interação (Atualizada)

```json
{
  "student_id": "student_0000",
  "question_id": "concept_262_q4",
  "is_correct": false,
  "mastery_before": 0.5293,
  "probability": 0.503,
  "slip_eff": 0.1847,
  "guess_eff": 0.1245,
  "error_type": "misconception",
  "timestamp": "2025-11-16T15:56:10.986065",
  "mastery_after": 0.4986
}
```

**Novos campos na v4.0.0**:
- `slip_eff`: Slip efetivo ajustado por fatores cognitivos
- `guess_eff`: Guess efetivo ajustado por fatores cognitivos

---

## 5. Métricas da Simulação (Resultados Corrigidos)

### 5.1 Estatísticas Gerais

| Métrica | Valor (v3.0) | Valor (v4.0) | Mudança |
|---------|--------------|--------------|---------|
| Total de interações | 4,528 | 4,499 | -0.6% |
| Total de estudantes | 100 | 100 | 0% |
| Interações por estudante | 45.28 | 45.0 | -0.6% |
| Respostas corretas | 2,135 (47.2%) | 1,860 (41.3%) | -5.9% |
| Respostas incorretas | 2,393 (52.8%) | 2,639 (58.7%) | +5.9% |
| Tempo de processamento | 0.20s | 0.30s | +50% |

**Observações**:
- Acurácia reduziu de 47.2% para 41.3% com as correções
- Modelo mais conservador e realista após correções

---

### 5.2 Estatísticas de Domínio (Mastery)

| Métrica | Valor (v3.0) | Valor (v4.0) | Mudança |
|---------|--------------|--------------|---------|
| Média | 0.367 | 0.484 | +31.9% |
| Mediana | 0.364 | 0.250 | -31.3% |
| Desvio padrão | 0.126 | 0.442 | +250.8% |
| Mínimo | 0.058 | 0.018 | -69.0% |
| Máximo | 0.720 | 1.000 | +38.9% |

**Observações**:
- Maior variabilidade no domínio (desvio 4x maior)
- Distribuição mais bimodal: alguns estudantes chegam a 1.0, outros ficam perto de 0

---

### 5.3 Distribuição de Tipos de Erro

| Tipo de Erro | v3.0 (Qtd) | v3.0 (%) | v4.0 (Qtd) | v4.0 (%) | Mudança |
|--------------|------------|----------|------------|----------|---------|
| slip | 504 | 21.1% | 547 | 20.7% | -0.4% |
| misunderstanding | 495 | 20.7% | 516 | 19.6% | -1.1% |
| careless | 479 | 20.0% | 515 | 19.5% | -0.5% |
| misconception | 456 | 19.1% | 524 | 19.9% | +0.8% |
| incomplete | 459 | 19.2% | 537 | 20.3% | +1.1% |

**Observações**:
- Distribuição continua equilibrada
- Pequenas mudanças percentuais entre tipos

---

### 5.4 Desempenho por Perfil Cognitivo

| Perfil | Estudantes | Acurácia v3.0 | Acurácia v4.0 | Domínio v3.0 | Domínio v4.0 |
|--------|------------|---------------|---------------|--------------|--------------|
| **quick_learner** | 20 | 48.3% (±4.9%) | **49.5%** (±24.2%) | 0.518 (±0.057) | **0.657** (±0.304) |
| **balanced** | 30 | 51.2% (±9.6%) | 43.0% (±24.6%) | 0.360 (±0.045) | 0.499 (±0.319) |
| **careful** | 20 | 47.4% (±8.3%) | 42.5% (±35.6%) | 0.345 (±0.051) | 0.457 (±0.408) |
| **intuitive** | 10 | 43.6% (±8.0%) | 37.7% (±24.6%) | 0.343 (±0.032) | 0.419 (±0.315) |
| **logical** | 10 | 49.8% (±8.2%) | 30.5% (±26.8%) | 0.373 (±0.041) | 0.401 (±0.336) |
| **struggling** | 10 | 33.4% (±9.4%) | **25.0%** (±10.1%) | 0.132 (±0.020) | **0.186** (±0.152) |

**Observações importantes**:
- **quick_learner**: Agora tem claramente o melhor desempenho (49.5% acurácia, 0.657 domínio)
- **struggling**: Pior desempenho acentuado (25.0% acurácia, 0.186 domínio)
- **Maior variabilidade**: Desvios padrão aumentaram significativamente
- **logical**: Surpreendente queda de desempenho (30.5% acurácia)

---

### 5.5 Correlação entre Parâmetros e Desempenho (v4.0)

#### Correlação com Acurácia

| Parâmetro | v3.0 | v4.0 | Mudança |
|-----------|------|------|---------|
| **memory_capacity** | 0.246 | **0.252** | +0.006 |
| **mastery_init** | **0.592** | 0.210 | -0.382 |
| **tech_familiarity** | 0.350 | 0.201 | -0.149 |
| **learn_rate** | 0.183 | 0.199 | +0.016 |
| **reading_skill** | 0.088 | 0.170 | +0.082 |
| **learning_consistency** | 0.196 | 0.167 | -0.029 |
| **logic_skill** | 0.331 | 0.086 | -0.245 |
| **slip** | -0.336 | -0.058 | +0.278 |
| **guess** | -0.269 | -0.046 | +0.223 |

#### Correlação com Domínio Médio

| Parâmetro | v3.0 | v4.0 | Mudança |
|-----------|------|------|---------|
| **tech_familiarity** | **0.868** | 0.328 | -0.540 |
| **memory_capacity** | **0.849** | 0.345 | -0.504 |
| **learn_rate** | **0.815** | 0.322 | -0.493 |
| **mastery_init** | 0.714 | 0.290 | -0.424 |
| **logic_skill** | 0.574 | 0.192 | -0.382 |
| **learning_consistency** | 0.565 | 0.219 | -0.346 |
| **guess** | -0.485 | -0.127 | +0.358 |
| reading_skill | 0.331 | 0.165 | -0.166 |
| **slip** | -0.256 | -0.054 | +0.202 |

**Mudanças drásticas nas correlações**:
- `mastery_init`: De 0.592 para 0.210 (perdeu força como preditor)
- `memory_capacity`: Agora é o fator mais importante (0.252)
- Correlações em geral diminuíram, indicando maior complexidade no modelo

---

### 5.6 Top 5 Fatores Mais Importantes (v4.0)

Baseado na correlação com acurácia:

1. **memory_capacity** (0.252): Capacidade de retenção agora é crucial
2. **mastery_init** (0.210): Ainda importante, mas menos determinante
3. **tech_familiarity** (0.201): Familiaridade tecnológica mantém relevância
4. **learn_rate** (0.199): Taxa de aprendizagem ganhou importância
5. **reading_skill** (0.170): Habilidade de leitura mais relevante

---

## 6. Análise Comparativa: v3.0 vs v4.0

### 6.1 Impacto das Correções

| Aspecto | v3.0 (Antes) | v4.0 (Depois) | Análise |
|---------|--------------|---------------|---------|
| **Modelo BKT** | Heurístico | Clássico (Bayesiano) | Mais fundamentado |
| **Acurácia geral** | 47.2% | 41.3% | Mais realista/conservador |
| **Variabilidade** | Baixa | Alta | Estudantes mais distintos |
| **Fator chave** | mastery_init | memory_capacity | Mudança de paradigma |
| **Correlações** | Altas | Moderadas | Modelo mais complexo |
| **Progressão** | Linear | Não-linear | Curvas de aprendizagem |

### 6.2 Insights das Mudanças

1. **Modelo mais realista**: Acurácia menor reflete maior dificuldade real
2. **Memória é crucial**: `memory_capacity` emergiu como fator principal
3. **Menos determinismo**: Correlações mais baixas indicam comportamento mais complexo
4. **Diferenças ampliadas**: Perfis agora se comportam mais distintamente
5. **Aprendizagem visível**: `current_mastery` permite ver progresso real

### 6.3 Validação das Correções

✅ **Correção A (current_mastery)**: Permitiu curvas de aprendizagem visíveis  
✅ **Correção B (Bayes)**: Modelo mais fundamentado academicamente  
✅ **Correção C (slip/guess efetivos)**: Fatores cognitivos bem modelados  
✅ **Correção D (ruído na prob)**: Estado interno limpo  
✅ **Correção E (decay ajustado)**: Esquecimento mais realista  

---

## 7. Conclusões e Insights

### 7.1 Validação do Modelo v4.0

1. **Fundamentação teórica**: Alinhado com BKT clássico (Corbett & Anderson, 1995)
2. **Comportamento realista**: Estudantes mostram progresso e esquecimento
3. **Diversidade acentuada**: Perfis comportam-se de forma mais distinta
4. **Complexidade aumentada**: Menos previsível, mais realista

### 7.2 Fatores Críticos de Sucesso (v4.0)

1. **Capacidade de memória** (`memory_capacity`): Principal preditor de sucesso
2. **Domínio inicial** (`mastery_init`): Ainda relevante, mas não dominante
3. **Familiaridade tecnológica**: Importante para ambiente Linux
4. **Taxa de aprendizagem**: Determina velocidade de progressão
5. **Habilidade de leitura**: Mais relevante que lógica (mudança significativa)

### 7.3 Descobertas Inesperadas

1. **Logic skill perdeu força**: De 2º para 8º fator mais importante
2. **Reading skill ganhou**: De último para 5º lugar
3. **Quick_learner destacou-se**: Agora claramente superior aos outros
4. **Logical profile sofreu**: Pior desempenho inesperado
5. **Variabilidade explodiu**: Desvios padrão 4x maiores

### 7.4 Próximos Passos

- Análise detalhada do perfil logical (por que baixo desempenho?)
- Validação com dados reais de estudantes
- Calibração fina dos pesos dos fatores cognitivos
- Experimentação com diferentes cenários de aprendizagem
- Geração de datasets experimentais com fatores independentes

---

## 8. Arquivos Gerados

| Arquivo | Descrição | Versão | Tamanho |
|---------|-----------|--------|---------|
| `data/output/notebooks/geracao_perfis/profiles.json` | 6 perfis cognitivos | 1.0.0 | ~2 KB |
| `data/output/notebooks/geracao_estudantes/students.json` | 100 estudantes sintéticos | 1.0.0 | ~50 KB |
| `data/output/notebooks/simulacao_interacoes/interactions_bkt.json` | 4,499 interações BKT corrigidas | 4.0.0 | 1.45 MB |

---

## 9. Referências Técnicas

### 9.1 Modelo BKT Clássico

```
P(correct) = P(L) * (1 - slip) + (1 - P(L)) * guess

Update Bayesiano:
  Se acertou: P(L|correct) = P(L)*(1-slip) / [P(L)*(1-slip) + (1-P(L))*guess]
  Se errou:   P(L|wrong)   = P(L)*slip / [P(L)*slip + (1-P(L))*(1-guess)]

Transição: P(L_next) = P(L|obs) + (1 - P(L|obs)) * learn_rate
```

**Referência**: Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the acquisition of procedural knowledge. *User Modeling and User-Adapted Interaction*, 4(4), 253-278.

### 9.2 Extensões Implementadas (v4.0)

1. **Parâmetros efetivos**: Slip e guess ajustados por fatores cognitivos
2. **Update Bayesiano**: Implementação exata da fórmula clássica
3. **Decay temporal controlado**: Só para gaps > 6h
4. **Ruído observacional**: Na probabilidade, não no estado
5. **Progressão realista**: Usando current_mastery atualizado

---

**Documento atualizado em**: 16 de dezembro de 2025  
**Versão do pipeline**: 4.0.0 (com correções BKT)  
**Seed de reprodutibilidade**: 42  
**Total de correções implementadas**: 5
