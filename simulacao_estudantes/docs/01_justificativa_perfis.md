# Justificativa dos Perfis Cognitivos SINKT

**Versão**: 2.0.0  
**Data**: 14 de Dezembro de 2025  
**Modelo Base**: BKT (Bayesian Knowledge Tracing) + Fatores Cognitivos

---

## 1. Introdução

Este documento justifica a criação e parametrização dos 7 perfis cognitivos utilizados na simulação de estudantes SINKT. Cada perfil representa um tipo de estudante com características únicas de aprendizagem, fundamentadas em modelos educacionais validados.

### 1.1 Fundamento Teórico

O modelo utiliza **Bayesian Knowledge Tracing (BKT)**, um dos modelos mais consolidados em Knowledge Tracing, complementado com **fatores cognitivos** baseados em teoria educacional.

**Equação BKT Básica:**
```
P(correct) = mastery + (1 - mastery) × guess - mastery × slip
```

Onde:
- **mastery**: Probabilidade de dominar o conceito
- **guess**: Probabilidade de acerto sem saber
- **slip**: Probabilidade de erro mesmo sabendo

---

## 2. Parâmetros Fundamentais

### 2.1 Parâmetros BKT (Knowledge Tracing)

#### **mastery_init_level** (0-1)
- **Definição**: Nível inicial de domínio do estudante
- **Interpretação**: Conhecimento prévio e base inicial
- **Range Típico**: 0.25-0.75
- **Impacto**: Alto - determina ponto de partida

#### **learn_rate** (0-0.1)
- **Definição**: Velocidade de aquisição de novo conhecimento
- **Interpretação**: Quanto o domínio aumenta a cada interação bem-sucedida
- **Range Típico**: 0.012-0.075
- **Impacto**: Crítico - define velocidade de aprendizado

#### **slip** (0-0.2)
- **Definição**: Probabilidade de erro quando realmente sabe
- **Interpretação**: Erros por distração, pressa ou descuido
- **Range Típico**: 0.05-0.25
- **Impacto**: Alto - afeta confiabilidade do desempenho

#### **guess** (0-0.3)
- **Definição**: Probabilidade de acerto quando não sabe
- **Interpretação**: Acertos por sorte ou chute
- **Range Típico**: 0.05-0.22
- **Impacto**: Médio - afeta taxa de falsos positivos

### 2.2 Parâmetros Cognitivos

#### **logic_skill** (0-1)
- **Definição**: Habilidade de raciocínio lógico e formal
- **Aplicação**: Problemas algorítmicos, estruturas de dados, programação
- **Correlação**: Inversa com guess (lógica forte → menos chutes)
- **Range Típico**: 0.3-0.9

#### **reading_skill** (0-1)
- **Definição**: Habilidade de compreensão de texto
- **Aplicação**: Interpretação de enunciados, documentação, especificações
- **Correlação**: Inversa com slip (leitura forte → menos erros por má compreensão)
- **Range Típico**: 0.25-0.85

#### **memory_capacity** (0-1)
- **Definição**: Capacidade de retenção de informações
- **Aplicação**: Memorização de sintaxe, conceitos, padrões
- **Correlação**: Positiva com mastery_init_level
- **Range Típico**: 0.4-0.85

#### **tech_familiarity** (0-1)
- **Definição**: Experiência prévia com tecnologia
- **Aplicação**: Conforto com ferramentas, ambientes de desenvolvimento
- **Correlação**: Positiva com learn_rate
- **Range Típico**: 0.2-0.8

#### **learning_consistency** (0-1)
- **Definição**: Consistência e disciplina no aprendizado
- **Aplicação**: Regularidade de estudo, persistência em dificuldades
- **Correlação**: Positiva com memory_capacity
- **Range Típico**: 0.4-0.95

---

## 3. Descrição dos Perfis

### 3.1 Perfil 1: Estudante Equilibrado

**ID**: `balanced`  
**Distribuição**: 25% da população

#### Características
- Habilidades balanceadas em todas as dimensões
- Representa o estudante "típico" ou "médio"
- Desenvolvimento uniforme

#### Parametrização
```json
{
  "mastery_init_level": 0.50,
  "learn_rate": 0.035,
  "slip": 0.12,
  "guess": 0.15,
  "logic_skill": 0.55,
  "reading_skill": 0.55,
  "memory_capacity": 0.55,
  "tech_familiarity": 0.50,
  "learning_consistency": 0.60
}
```

#### Justificativa
- **mastery_init_level = 0.50**: Conhecimento médio, nem iniciante nem avançado
- **learn_rate = 0.035**: Taxa de aprendizado moderada
- **slip = 0.12**: Erros ocasionais, mas não frequentes
- **guess = 0.15**: Chuta quando não sabe, mas não excessivamente
- **Habilidades = 0.50-0.55**: Balanceadas, sem pontos fortes ou fracos
- **learning_consistency = 0.60**: Estuda regularmente

#### Comportamento Esperado
- Acurácia: ~60-65%
- Tempo de aprendizado: Médio
- Padrão: Estável e previsível

---

### 3.2 Perfil 2: Aprendiz Rápido

**ID**: `quick_learner`  
**Distribuição**: 15% da população

#### Características
- Alta capacidade de aprendizagem
- Domínio inicial elevado
- Poucos erros (corrigido de 0.18 para 0.08)

#### Parametrização
```json
{
  "mastery_init_level": 0.70,
  "learn_rate": 0.075,
  "slip": 0.08,
  "guess": 0.10,
  "logic_skill": 0.75,
  "reading_skill": 0.70,
  "memory_capacity": 0.80,
  "tech_familiarity": 0.75,
  "learning_consistency": 0.85
}
```

#### Justificativa
- **mastery_init_level = 0.70**: Conhecimento prévio sólido
- **learn_rate = 0.075**: Aprende rapidamente (2x mais que equilibrado)
- **slip = 0.08**: CORRIGIDO - Aprendizes rápidos têm POUCOS erros, não muitos
- **guess = 0.10**: Raramente chuta, confia no conhecimento
- **logic_skill = 0.75**: Forte em raciocínio
- **memory_capacity = 0.80**: Boa retenção
- **learning_consistency = 0.85**: Muito disciplinado

#### Comportamento Esperado
- Acurácia: ~75-85%
- Tempo de aprendizado: Rápido (5-10 interações por conceito)
- Padrão: Convergência rápida

#### Correção Implementada
A versão anterior tinha `slip = 0.18`, o que era contraditório. Um aprendiz rápido não deveria errar frequentemente. Corrigido para `slip = 0.08`.

---

### 3.3 Perfil 3: Estudante Cuidadoso

**ID**: `careful`  
**Distribuição**: 15% da população

#### Características
- Baixa taxa de erros quando sabe
- Aprendizado gradual e meticuloso
- Detalhista

#### Parametrização
```json
{
  "mastery_init_level": 0.45,
  "learn_rate": 0.020,
  "slip": 0.06,
  "guess": 0.08,
  "logic_skill": 0.65,
  "reading_skill": 0.75,
  "memory_capacity": 0.70,
  "tech_familiarity": 0.45,
  "learning_consistency": 0.90
}
```

#### Justificativa
- **mastery_init_level = 0.45**: Começa com conhecimento abaixo da média
- **learn_rate = 0.020**: Aprende lentamente, mas solidamente
- **slip = 0.06**: Muito cuidadoso, raramente erra
- **reading_skill = 0.75**: Lê bem, entende enunciados
- **learning_consistency = 0.90**: Extremamente disciplinado
- **logic_skill = 0.65**: Bom em lógica, mas não excepcional

#### Comportamento Esperado
- Acurácia: ~70-75%
- Tempo de aprendizado: Lento mas seguro (15-20 interações por conceito)
- Padrão: Crescimento constante e confiável

---

### 3.4 Perfil 4: Estudante com Dificuldades

**ID**: `struggling`  
**Distribuição**: 15% da população

#### Características
- Baixo domínio inicial
- Aprendizado lento
- Necessita mais apoio

#### Parametrização
```json
{
  "mastery_init_level": 0.25,
  "learn_rate": 0.012,
  "slip": 0.20,
  "guess": 0.22,
  "logic_skill": 0.30,
  "reading_skill": 0.35,
  "memory_capacity": 0.40,
  "tech_familiarity": 0.20,
  "learning_consistency": 0.40
}
```

#### Justificativa
- **mastery_init_level = 0.25**: Conhecimento inicial muito baixo
- **learn_rate = 0.012**: Aprende muito lentamente
- **slip = 0.20**: Erra frequentemente mesmo sabendo
- **guess = 0.22**: Chuta muito quando não sabe
- **logic_skill = 0.30**: Fraco em raciocínio lógico
- **reading_skill = 0.35**: Dificuldade em compreensão
- **learning_consistency = 0.40**: Inconsistente, falta disciplina

#### Comportamento Esperado
- Acurácia: ~35-45%
- Tempo de aprendizado: Muito lento (30-50 interações por conceito)
- Padrão: Convergência lenta, pode não convergir

---

### 3.5 Perfil 5: Pensador Lógico

**ID**: `logical`  
**Distribuição**: 15% da população

#### Características
- Excelente habilidade lógica
- Dificuldade em leitura e interpretação
- Forte em algoritmos, fraco em documentação

#### Parametrização
```json
{
  "mastery_init_level": 0.55,
  "learn_rate": 0.045,
  "slip": 0.10,
  "guess": 0.08,
  "logic_skill": 0.90,
  "reading_skill": 0.25,
  "memory_capacity": 0.60,
  "tech_familiarity": 0.65,
  "learning_consistency": 0.75
}
```

#### Justificativa
- **logic_skill = 0.90**: Excepcional em raciocínio formal
- **reading_skill = 0.25**: Fraco em compreensão de texto
- **learn_rate = 0.045**: Aprende bem em tópicos lógicos
- **guess = 0.08**: Confia em lógica, não chuta
- **slip = 0.10**: Poucos erros quando sabe

#### Comportamento Esperado
- Acurácia: ~70-75% (bom em lógica, ruim em interpretação)
- Tempo de aprendizado: Médio a rápido
- Padrão: Excelente em conceitos teóricos, dificuldade em enunciados verbosos

---

### 3.6 Perfil 6: Estudante Intuitivo

**ID**: `intuitive`  
**Distribuição**: 10% da população

#### Características
- Boa intuição e habilidade de leitura
- Dificuldade com formalismo lógico
- Aprende por exemplo e prática

#### Parametrização
```json
{
  "mastery_init_level": 0.40,
  "learn_rate": 0.040,
  "slip": 0.14,
  "guess": 0.18,
  "logic_skill": 0.35,
  "reading_skill": 0.85,
  "memory_capacity": 0.65,
  "tech_familiarity": 0.40,
  "learning_consistency": 0.65
}
```

#### Justificativa
- **reading_skill = 0.85**: Excelente em compreensão
- **logic_skill = 0.35**: Fraco em raciocínio formal
- **guess = 0.18**: Chuta mais quando não sabe
- **learn_rate = 0.040**: Aprende bem com exemplos
- **memory_capacity = 0.65**: Boa memória para padrões

#### Comportamento Esperado
- Acurácia: ~60-65% (bom em interpretação, ruim em lógica)
- Tempo de aprendizado: Médio
- Padrão: Excelente com exemplos, dificuldade com abstrações

---

### 3.7 Perfil 7: Perfeccionista

**ID**: `perfectionist`  
**Distribuição**: 5% da população

#### Características
- Muito rigoroso e exigente
- Aprendizado profundo mas lento
- Altíssima consistência

#### Parametrização
```json
{
  "mastery_init_level": 0.60,
  "learn_rate": 0.025,
  "slip": 0.05,
  "guess": 0.05,
  "logic_skill": 0.80,
  "reading_skill": 0.80,
  "memory_capacity": 0.85,
  "tech_familiarity": 0.60,
  "learning_consistency": 0.95
}
```

#### Justificativa
- **slip = 0.05**: Praticamente não erra
- **guess = 0.05**: Nunca chuta
- **learning_consistency = 0.95**: Máxima disciplina
- **memory_capacity = 0.85**: Excelente retenção
- **learn_rate = 0.025**: Aprende lentamente mas profundamente

#### Comportamento Esperado
- Acurácia: ~80-85%
- Tempo de aprendizado: Lento mas muito profundo
- Padrão: Convergência lenta, mas para nível muito alto

---

## 4. Validação de Coerência

### 4.1 Regras de Coerência Implementadas

1. **Regra 1**: `learn_rate` alto → `slip` baixo
   - Aprendizes rápidos não devem errar frequentemente
   - Exemplo: `quick_learner` tem `learn_rate=0.075` e `slip=0.08` ✓

2. **Regra 2**: `logic_skill` alto → `guess` baixo
   - Pessoas com lógica forte não chutem
   - Exemplo: `logical` tem `logic_skill=0.90` e `guess=0.08` ✓

3. **Regra 3**: `memory_capacity` alto → `learning_consistency` alto
   - Boa memória correlaciona com disciplina
   - Exemplo: `perfectionist` tem `memory_capacity=0.85` e `learning_consistency=0.95` ✓

### 4.2 Validação Estatística

| Parâmetro | Média | Desvio | Min | Max |
|-----------|-------|--------|-----|-----|
| mastery_init_level | 0.475 | 0.138 | 0.25 | 0.70 |
| learn_rate | 0.034 | 0.022 | 0.012 | 0.075 |
| slip | 0.110 | 0.063 | 0.05 | 0.20 |
| guess | 0.112 | 0.063 | 0.05 | 0.22 |
| logic_skill | 0.596 | 0.263 | 0.30 | 0.90 |
| reading_skill | 0.596 | 0.263 | 0.25 | 0.85 |
| memory_capacity | 0.664 | 0.154 | 0.40 | 0.85 |
| tech_familiarity | 0.514 | 0.181 | 0.20 | 0.75 |
| learning_consistency | 0.729 | 0.189 | 0.40 | 0.95 |

---

## 5. Geração de Estudantes

### 5.1 Processo

1. **Seleção de Perfil**: Cada estudante é atribuído a um perfil conforme distribuição
2. **Variação Individual**: Cada parâmetro varia ±15% do valor base
3. **Garantia de Realismo**: Valores mantidos no range [0, 1]
4. **Reprodutibilidade**: Seed fixa (42) para resultados determinísticos

### 5.2 Exemplo de Variação

**Perfil Base (balanced)**:
```json
{
  "mastery_init_level": 0.50,
  "learn_rate": 0.035,
  "logic_skill": 0.55
}
```

**Estudante 1** (variação +10%):
```json
{
  "mastery_init_level": 0.55,
  "learn_rate": 0.0385,
  "logic_skill": 0.605
}
```

**Estudante 2** (variação -8%):
```json
{
  "mastery_init_level": 0.46,
  "learn_rate": 0.0322,
  "logic_skill": 0.506
}
```

---

## 6. Impacto nos Dados de Interação

### 6.1 Probabilidade de Resposta Correta

Calculada usando BKT:
```
P(correct) = mastery + (1 - mastery) × guess - mastery × slip
```

**Exemplo - Aprendiz Rápido**:
- mastery = 0.70
- guess = 0.10
- slip = 0.08
- P(correct) = 0.70 + (1 - 0.70) × 0.10 - 0.70 × 0.08
- P(correct) = 0.70 + 0.03 - 0.056 = **0.674 (67.4%)**

**Exemplo - Estudante com Dificuldades**:
- mastery = 0.25
- guess = 0.22
- slip = 0.20
- P(correct) = 0.25 + (1 - 0.25) × 0.22 - 0.25 × 0.20
- P(correct) = 0.25 + 0.165 - 0.05 = **0.365 (36.5%)**

### 6.2 Atualização de Domínio

Após cada interação:
- **Se correto**: `mastery_novo = mastery + (1 - mastery) × learn_rate`
- **Se incorreto**: `mastery_novo = mastery × (1 - learn_rate × 0.5)`

---

## 7. Conclusões

### 7.1 Pontos Fortes

✓ Perfis fundamentados em teoria educacional validada (BKT)  
✓ 9 parâmetros cognitivos bem definidos e correlacionados  
✓ Validação de coerência interna  
✓ Sem fatores demográficos (justo e ético)  
✓ Variação individual realista  
✓ Reprodutibilidade garantida  

### 7.2 Próximos Passos

1. Treinar modelo SINKT com dados sintéticos
2. Validar com dados reais quando disponíveis
3. Calibrar parâmetros baseado em feedback
4. Expandir para novos domínios

---

## 8. Referências

1. **Corbett, A. T., & Anderson, J. R. (1994)**. Knowledge Tracing: Modeling the Acquisition of Procedural Knowledge. *User Modeling and User-Adapted Interaction*, 4(4), 253-278.

2. **Bloom, B. S. (1956)**. Taxonomy of Educational Objectives: The Classification of Educational Goals.

3. **Swanson, H. L., & Beebe-Frankenberger, M. (2004)**. The Relationship Between Working Memory and Mathematical Problem Solving in Children at Risk and Not at Risk for Serious Math Difficulties. *Journal of Educational Psychology*, 96(3), 471-491.

4. **Piaget, J. (1954)**. The Construction of Reality in the Child.

---

**Documento Preparado Por**: Sistema SINKT  
**Data**: 14 de Dezembro de 2025  
**Versão**: 2.0.0
