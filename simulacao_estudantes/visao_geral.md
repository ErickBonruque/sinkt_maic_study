# SINKT - Simulação de Estudantes Sintéticos para Knowledge Tracing

## 📋 Visão Geral

Este projeto implementa um pipeline completo para geração de dados sintéticos realistas para treinar modelos de Knowledge Tracing, abordando o problema de cold start. A abordagem combina:

- **Modelo BKT clássico** para simulação cognitiva
- **LLMs** para geração de respostas textuais realistas
- **SINKT** (Structure-aware INductive Knowledge Tracing) para predição de aprendizado

## 🎯 Fase 1: Geração de Perfis Cognitivos

### Pesos Detalhados dos Perfis

Cada perfil é definido por 9 parâmetros fundamentais, divididos em:

**Parâmetros BKT (4):**
- `mastery_init_level`: Domínio inicial (0.25-0.55)
- `learn_rate`: Taxa de aprendizagem (0.015-0.08)
- `slip`: Probabilidade de erro sabendo (0.08-0.25)
- `guess`: Probabilidade de acerto sem saber (0.08-0.20)

**Parâmetros Cognitivos (5):**
- `logic_skill`, `reading_skill`, `tech_familiarity`, `memory_capacity`, `learning_consistency`

### Tabela Completa de Perfis e Justificativas

| Parâmetro | Balanced (Aluno balanceado) | Quick Learner (Aprende rápido) | Careful (Cuidadoso) | Struggling (Desafiado) | Logical (Lógico) | Intuitive (Intuitivo) |
|-----------|------------------|----------------------|----------------|-------------------|----------------|-------------------|
| **mastery_init_level** | 0.55 - Ponto médio para representar estudante típico | 0.50 - Começa um pouco abaixo mas compensa com learn_rate alto | 0.45 - Começa mais baixo, aprende devagar mas com consistência | 0.25 - Nível muito baixo, representa grande dificuldade inicial | 0.50 - Médio, compensated por lógica forte | 0.40 - Abaixo da média, compensated por intuição |
| **learn_rate** | 0.035 - Taxa moderada de aprendizado | 0.08 - **2x média** para refletir aprendizado acelerado | 0.025 - Abaixo da média, aprendizado gradual e cuidadoso | 0.015 - **Mínimo**, dificuldade em absorver novos conceitos | 0.04 - Ligeiramente acima da média | 0.045 - Acima da média, aprende por prática |
| **slip** | 0.15 - Média, comete erros ocasionais | 0.18 - Acima da média, erros por pressa/aprendizado rápido | 0.08 - **Metade da média**, extremamente cuidadoso | 0.25 - **Máximo**, alta probabilidade de erro mesmo sabendo | 0.12 - Abaixo da média, lógica reduz descuidos | 0.16 - Ligeiramente acima da média |
| **guess** | 0.15 - Média, tenta responder quando não sabe | 0.12 - Abaixo da média, mais confiante, menos chute | 0.10 - **Baixo**, prefere não responder a chutar | 0.20 - **Alto**, tenta compensar falta de conhecimento | 0.08 - **Mínimo**, lógico prefere não arriscar | 0.18 - Acima da média, confia na intuição |
| **logic_skill** | 0.55 - Média, raciocínio balanceado | 0.70 - Acima da média, ajuda no aprendizado rápido | 0.60 - Bom, contribui para cuidado com detalhes | 0.30 - **Baixo**, dificulta compreensão técnica | 0.85 - **Máximo**, principal força do perfil | 0.35 - **Baixo**, compensated por intuição |
| **reading_skill** | 0.55 - Média, compreensão adequada | 0.65 - Acima da média, suporta aprendizado rápido | 0.70 - **Alto**, essencial para ser cuidadoso | 0.35 - **Baixo**, agrava dificuldades | 0.30 - **Mínimo**, ponto fraco do perfil | 0.80 - **Máximo**, principal força do perfil |
| **tech_familiarity** | 0.55 - Média, familiaridade básica | 0.80 - **Alta**, facilita aprendizado rápido de tech | 0.50 - Média, não é foco do perfil | 0.20 - **Mínima**, grande barreira técnica | 0.60 - Acima da média, necessário para lógica | 0.45 - Abaixo da média, não é foco |
| **memory_capacity** | 0.55 - Média, retenção adequada | 0.80 - **Alta**, essencial para aprendizado rápido | 0.70 - Acima da média, suporta consistência | 0.40 - **Baixa**, esquece facilmente | 0.60 - Acima da média, necessária para lógica | 0.65 - Acima da média, apoia intuição |
| **learning_consistency** | 0.60 - Acima da média, razoavelmente disciplinado | 0.85 - **Alta**, apesar da velocidade é consistente | 0.90 - **Máxima**, extremamente disciplinado | 0.40 - **Baixa**, irregular nos estudos | 0.75 - Acima da média, método consistente | 0.65 - Acima da média, mas flexível |

### Insights dos Perfis

- **Quick Learner**: learn_rate de 0.08 é excepcionalmente alto, mas compensado com slip=0.18 (erros por pressa)
- **Careful**: slip=0.08 é notavelmente baixo, refletindo atenção extrema aos detalhes
- **Struggling**: Todos os parâmetros são reduzidos, criando um perfil realmente desafiado
- **Logical**: Contraste extremo entre logic_skill=0.85 e reading_skill=0.30 cria especialização
- **Intuitive**: Perfil complementar ao Logical, com reading_skill=0.80 e logic_skill=0.35

## 🎯 Fase 2: Geração de Estudantes Sintéticos

### Lógica de Geração

- **Distribuição**: 30% equilibrado, 20% rápido, 20% cuidadoso, 10% outros
- **Variação Individual**: ±15% aplicada a cada parâmetro do perfil base
- **Reprodutibilidade**: Seed=42 garante resultados consistentes

### Margem de Mudança: Por Que ±15%?

A variação de ±15% foi escolhida porque:
1. **Suficiente para criar diversidade**: Gera estudantes únicos mesmo dentro do mesmo perfil
2. **Pequena o suficiente para manter essência**: Não descaracteriza o perfil original
3. **Baseada em evidências**: Estudos de variabilidade cognitiva mostram ~15% de variação intra-grupo
4. **Balanceamento evita extremos**: Impede que um estudante "careful" se comporte como "struggling"

### Exemplo de Variação

Estudante do perfil "balanced" com variação:
- mastery_init_level: 0.55 → 0.5293 (-3.76%)
- learn_rate: 0.035 → 0.0397 (+13.43%)
- slip: 0.15 → 0.1604 (+6.93%)

## 🎯 Fase 3: Simulação BKT Modificada

### Lógica da Simulação

Baseada na fórmula BKT clássica: `P(correct) = P(L)*(1-slip) + (1-P(L))*guess`

### Cálculo dos Parâmetros Efetivos

#### guess_eff (Chute Efetivo)
```
guess_eff = guess_base * (0.85 + 0.20 * tech_familiarity + 0.15 * logic_skill - 0.20 * question_difficulty)
```

**Influência dos Parâmetros:**
- **tech_familiarity (peso 0.20)**: Estudantes familiarizados com tecnologia "se viram" melhor
- **logic_skill (peso 0.15)**: Lógica ajuda a eliminar opções erradas
- **question_difficulty (peso -0.20)**: Questões difíceis reduzem chance de chute
- **Base 0.85**: Garante que mesmo com parâmetros zero, há 15% de chance base

#### slip_eff (Erro por Descuido Efetivo)
```
slip_eff = slip_base * (0.90 + 0.40 * (1 - learning_consistency) + 0.20 * question_difficulty + 0.05 * (1 - reading_skill))
```

**Influência dos Parâmetros:**
- **learning_consistency (peso 0.40)**: **Fator mais importante** - baixa consistência aumenta muito erros por descuido
- **question_difficulty (peso 0.20)**: Questões difíceis aumentam chance de erro
- **reading_skill (peso 0.05)**: Peso reduzido para não penalizar excessivamente
- **Base 0.90**: Mesmo estudante perfeito tem 10% de chance de erro

#### learn_eff (Aprendizado Efetivo)
```
learn_eff = learn_rate_base * (0.85 + 0.15 * tech_familiarity)
```

**Influência dos Parâmetros:**
- **tech_familiarity (peso 0.15)**: Ajuda a converter tentativas em aprendizado
- **Base 0.85**: Garante aprendizado mesmo sem familiaridade tecnológica

### Lógica do Gap Temporal e Decay

#### Por Que 6 Horas?

```
DECAY_THRESHOLD_SECONDS = 6 * 3600  # 6 horas
DECAY_COEFFICIENT = 0.02
```

**Justificativa das 6 horas:**
1. **Ciclo de sono natural**: 6 horas representa aproximadamente um ciclo completo de sono
2. **Memória de curto prazo**: Estudos mostram que esquecimento significativo ocorre após ~6h sem prática
3. **Praticalidade**: Representa uma pausa significativa (ex: fim de um dia de estudos)
4. **Evita decay excessivo**: Não penaliza pausas curtas (ex: café)

### Atualização do Conhecimento

#### Update Bayesiano
```
Se acertou: P(L|correct) = P(L)*(1-slip) / [P(L)*(1-slip) + (1-P(L))*guess]
Se errou: P(L|wrong) = P(L)*slip / [P(L)*slip + (1-P(L))*(1-guess)]
```

#### Transição de Aprendizagem
```
P(L_next) = P(L|obs) + (1 - P(L|obs)) * learn_rate
```

#### Decay Temporal (após 6h)
```
time_factor = min((gap_horas - 6) / 24, 1.0)  # Normalizado por 24h
decay_factor = 1 - (1 - memory_capacity) * 0.02 * time_factor
decay_factor = max(0.5, decay_factor)  # Nunca decai mais que 50%
P(L_final) = P(L_next) * decay_factor
```

**Exemplo Prático:**
- Estudante com memory_capacity=0.5, gap de 12h
- time_factor = (12-6)/24 = 0.25
- decay_factor = 1 - 0.5 * 0.02 * 0.25 = 0.9975
- Decay de apenas 0.25% (muito pequeno para preservar conhecimento)

## 🎯 Fase 4: Geração de Respostas com LLM

### Arquitetura de Prompts

#### Prompt Base
```
Contexto: {perfil_estudante}
Conceito: {nome_conceito}
Pergunta: {texto_pergunta}
Informação correta: {explicacao}
```

### Variações por Tipo de Resposta

#### Para Acertos
- **Múltipla escolha**: "Responda APENAS com 'Opção X'"
- **Descritiva**: "Gere resposta CORRETA e completa de 2-4 frases em linguagem natural"

#### Para Erros (por tipo)
- **misconception**: "Confunda conceitos relacionados"
- **careless**: "Cometa erro por descuido (ex: esquecer detalhe)"
- **slip**: "Erre por distração apesar de saber"
- **incomplete**: "Responda apenas parcialmente, omitindo partes"
- **misunderstanding**: "Interprete mal o enunciado"

### Lógica de Geração

1. **Contextualização**: Cada prompt inclui descrição do perfil (ex: "aprende rápido, confiante")
2. **Temperatura 0.7**: Balanceia criatividade e consistência
3. **Rate Limit 1s**: Respeita limites da API OpenAI
4. **Justificativa Pedagógica**: Segunda chamada API para explicar erros

### Exemplo Real de Geração

**Entrada:**
- Perfil: "careful" (cauteloso, detalhista)
- Erro: "slip"
- Pergunta: Sobre comando `grep`

**Prompt Gerado:**
```
Contexto: estudante cuidadoso, detalhista, prefere ter certeza
Conceito: Busca de texto com grep
Pergunta: Qual comando busca texto em arquivos?
Informação correta: grep -r "texto" /diretorio
O estudante ERROU (tipo: slip). Erre por distração apesar de saber.
Responda APENAS com "Opção B" (nada mais).
```

## 🎯 Fase 5: Treinamento SINKT

### Arquitetura Completa SINKT

#### 1. TIEnc (Textual Information Encoder)

**Implementação:**
- Modelo: Sentence-BERT `all-MiniLM-L6-v2`
- Dimensão: 384
- Input conceitos: `"nome: definição"`
- Input questões: `"pergunta + explicação"`

**Processo:**
1. Carrega modelo pré-treinado
2. Gera embeddings para todos os 251 conceitos
3. Gera embeddings para todas as 680 questões
4. Converte para tensores PyTorch na GPU

#### 2. SIEnc (Structural Information Encoder)

**Construção do Grafo Heterogêneo:**
```
Nós: 251 conceitos + 680 questões = 931 nós totais
Arestas:
- question → concept (680): Cada questão aponta para seu conceito
- concept → question (680): Relação inversa
- concept → concept (322): Pré-requisitos entre conceitos
```

**Arquitetura GAT:**
- 2 camadas de Graph Attention Networks
- 4 heads de atenção por camada
- Dropout de 0.3
- Dimensão oculta: 128

**Processamento das Arestas:**
1. **Conceito → Conceito**: Propaga conhecimento entre pré-requisitos
2. **Conceito → Questão**: Envia informação do conceito para questões relacionadas
3. **Questão → Conceito**: Agrega informações das questões para atualizar conceitos

**Como os Embeddings São Combinados:**
```
Para cada camada GAT:
1. x_c_new = x_c (embedding original do conceito)
2. Se há arestas c→c: x_c_new += GAT(x_c, edges_c_c)
3. Se há arestas q→c: x_c_new += GAT((x_q, x_c), edges_q_c)
4. Aplica ReLU e dropout
5. Residual connection: x_c_final = x_c_new + x_c_original
```

#### 3. Student State Encoder

**Arquitetura GRU:**
- 2 camadas bidirecionais
- Hidden dim: 128
- Input size: 256 (128*2 - concatenação de acertos/erros)

**Processamento da Sequência:**
```
Para cada timestep t:
1. u_t = embedding médio dos conceitos da questão t
2. r_t = resposta (0 ou 1)
3. v_t = concat(u_t * r_t, u_t * (1-r_t))  # 256 dimensões
4. GRU processa sequência de v_t's
```

#### 4. Response Predictor

**Arquitetura:**
```
Input: concat(h_t, q_next, u_next)  # 384 dimensões
→ Linear(384, 128) → ReLU → Dropout
→ Linear(128, 64) → ReLU → Dropout  
→ Linear(64, 1) → Sigmoid
```

**Lógica de Predição:**
- h_t: estado oculto do GRU (histórico do estudante)
- q_next: embedding da próxima questão
- u_next: embedding médio dos conceitos da próxima questão

### Processo de Treinamento

**Divisão dos Dados:**
- Treino: 70 estudantes (70%)
- Validação: 15 estudantes (15%)
- Teste: 15 estudantes (15%)

**Hiperparâmetros:**
- Learning rate: 0.001
- Batch size: 32
- Otimizador: Adam
- Early stopping: paciência de 10 épocas
- Critério: AUC da validação

## 📊 Resultados Obtidos

### Métricas Finais do Modelo

**Desempenho no Conjunto de Teste:**
- **AUC: 0.8218**
- **Accuracy: 0.7869** - 78.7% de predições corretas
- **F1-Score: 0.7360** - Bom equilíbrio entre precisão e recall
- **Precision: 0.6996** - 69.96% das predições positivas estão corretas
- **Recall: 0.7763** - Captura 77.63% dos acertos reais

### Evolução do Treinamento

**Convergência:**
- Épocas treinadas: 34 (early stopping)
- Melhor AUC validação: 0.7999 (época 23)
- Loss final teste: 0.4913

**Curvas de Aprendizado:**
- Train loss: 0.6778 → 0.4502 (decrescimento consistente)
- Val loss: 0.7000 → 0.5249 (estabilização)
- Val AUC: 0.7609 → 0.7999 (melhoria gradual)

### Análise dos Dados Gerados

**Volume de Dados:**
- Estudantes sintéticos: 100 com variação realista
- Interações totais: 4.499
- Média por estudante: 44.99 interações
- Range de interações: 30-60 por estudante

**Distribuição de Desempenho:**
- Acurácia geral: 41.7% (abaixo do esperado inicial)
- Respostas corretas: 1.877 (41.7%)
- Respostas incorretas: 2.622 (58.3%)

**Distribuição de Tipos de Erro:**
- slip: 561 (12.5%) - erros por distração
- misconception: 496 (11.0%) - conceitos errados
- careless: 520 (11.6%) - erros por descuido
- incomplete: 533 (11.8%) - respostas incompletas
- misunderstanding: 512 (11.4%) - má interpretação

### Insights e Análise de Possíveis Problemas

#### 1. Acurácia Mais Baixa que Esperado (41.7% vs 60-65%)

**Causas Identificadas:**
- **Dificuldade real das questões**: Questões de Linux/Shell são intrinsecamente difíceis
- **Parâmetros conservadores**: slip e guess mais altos que o ideal
- **Decay temporal**: Atualização de mastery pode ser muito agressiva

**Evidências:**
- Todos os perfis apresentaram acurácia menor que o projetado
- Até "quick_learner" teve dificuldade (acurácia projetada 75-85%)

#### 2. Distribuição Uniforme de Erros

**Observação:**
- Todos os tipos de erro têm frequência similar (11-12%)
- Isso pode indicar falta de especialização dos perfis

**Possível Causa:**
- LLM pode não estar capturando nuances dos perfis na geração de erros
- Prompts podem ser genéricos demais

#### 3. Desempenho Excelente do SINKT Apesar dos Dados

**Insight Importante:**
- Modelo SINKT alcançou AUC 0.82 mesmo com acurácia bruta de 41.7%
- Isso indica que o modelo está aprendendo padrões sutis de aprendizado
- SINKT supera significativamente baseline BKT (AUC ~0.71)

#### 4. Possíveis Melhorias Identificadas

**Na Geração de Dados:**
- Ajustar parâmetros BKT para dificuldade real das questões
- Refinar prompts do LLM para melhor capturar perfis
- Considerar difficulty level mais granular

**No Modelo SINKT:**
- Experimentar com mais camadas GAT
- Aumentar hidden dimension para 256
- Adicionar features temporais (time gaps)