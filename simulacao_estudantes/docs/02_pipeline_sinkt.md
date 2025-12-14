# Pipeline SINKT - Guia Completo

**Versão**: 1.0.0  
**Data**: 14 de Dezembro de 2025

---

## 1. Visão Geral

O pipeline SINKT (Structure-aware Inductive Knowledge Tracing) implementa um processo de 4 etapas para gerar dados sintéticos de estudantes em cenários de cold start:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE SINKT (4 ETAPAS)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ETAPA 1: Geração de Perfis Cognitivos                          │
│  ├─ 7 perfis com 9 parâmetros cada                              │
│  ├─ Baseado em BKT (Bayesian Knowledge Tracing)                 │
│  └─ Validação de coerência interna                              │
│         ↓                                                         │
│  ETAPA 2: Geração de Estudantes Sintéticos                      │
│  ├─ 100 estudantes com variação individual                      │
│  ├─ ±15% de variação por parâmetro                              │
│  └─ Distribuição balanceada entre perfis                        │
│         ↓                                                         │
│  ETAPA 3: Geração de Dados de Interação                         │
│  ├─ 3000-6000 interações (30-60 por estudante)                  │
│  ├─ Respostas simuladas via LLM                                 │
│  └─ Classificação de erros e explicações                        │
│         ↓                                                         │
│  ETAPA 4: Análise e Métricas                                    │
│  ├─ Validação de realismo                                       │
│  ├─ Análise de fatores influenciadores                          │
│  └─ Respostas às perguntas obrigatórias                         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Estrutura do Projeto

```
simulacao_estudantes/
├── 01_geracao_perfis.ipynb              # Etapa 1: Perfis Cognitivos
├── 02_geracao_estudantes.ipynb          # Etapa 2: Estudantes Sintéticos
├── 03_geracao_interacoes.ipynb          # Etapa 3: Dados de Interação
├── 04_analise_metricas.ipynb            # Etapa 4: Análise e Métricas
├── data/
│   ├── json/
│   │   ├── concepts_graph.json          # Grafo de conceitos (entrada)
│   │   └── questions_graph.json         # Grafo de questões (entrada)
│   └── output/
│       ├── profiles.json                # Saída Etapa 1
│       ├── students.json                # Saída Etapa 2
│       ├── interactions.json            # Saída Etapa 3
│       ├── analysis_report.json         # Saída Etapa 4
│       └── metrics_summary.json         # Resumo de métricas
├── docs/
│   ├── 01_justificativa_perfis.md       # Este documento
│   ├── 02_pipeline_sinkt.md             # Guia do pipeline
│   └── 03_respostas_obrigatorias.md     # Respostas às perguntas
├── requirements.txt                      # Dependências Python
└── README.md                             # Documentação geral
```

---

## 3. Detalhamento de Cada Etapa

### 3.1 Etapa 1: Geração de Perfis Cognitivos

**Arquivo**: `01_geracao_perfis.ipynb`

#### Objetivo
Criar 7 perfis cognitivos distintos que representam diferentes tipos de estudantes.

#### Processo
1. **Definição de Perfis**: 7 perfis com 9 parâmetros cada
2. **Validação**: Verificar ranges, IDs únicos, campos obrigatórios
3. **Análise de Coerência**: Validar relações entre parâmetros
4. **Cálculo de Estatísticas**: Média, desvio, min, max
5. **Salvamento**: JSON com metadados

#### Saída
- **Arquivo**: `data/output/profiles.json`
- **Conteúdo**:
  ```json
  {
    "metadata": {
      "num_profiles": 7,
      "parameters_count": 9,
      "model": "BKT + Cognitive Factors"
    },
    "profiles": {
      "balanced": { ... },
      "quick_learner": { ... },
      ...
    },
    "statistics": { ... }
  }
  ```

#### Tempo de Execução
~5-10 segundos

---

### 3.2 Etapa 2: Geração de Estudantes Sintéticos

**Arquivo**: `02_geracao_estudantes.ipynb`

#### Objetivo
Gerar 100 estudantes com variação individual dentro de cada perfil.

#### Processo
1. **Carregamento de Perfis**: Ler `profiles.json`
2. **Distribuição de Perfis**: Atribuir estudantes conforme distribuição
3. **Variação Individual**: Aplicar ±15% de variação a cada parâmetro
4. **Validação**: Verificar integridade dos dados
5. **Análise de Qualidade**: Calcular scores cognitivos e potencial
6. **Salvamento**: JSON com metadados

#### Distribuição de Perfis
- balanced: 25%
- quick_learner: 15%
- careful: 15%
- struggling: 15%
- logical: 15%
- intuitive: 10%
- perfectionist: 5%

#### Saída
- **Arquivo**: `data/output/students.json`
- **Conteúdo**:
  ```json
  {
    "metadata": {
      "num_students": 100,
      "generation_seed": 42,
      "individual_variation": 0.15,
      "quality_metrics": { ... }
    },
    "students": {
      "student_0000": { ... },
      "student_0001": { ... },
      ...
    }
  }
  ```

#### Tempo de Execução
~2-5 segundos

---

### 3.3 Etapa 3: Geração de Dados de Interação

**Arquivo**: `03_geracao_interacoes.ipynb`

#### Objetivo
Gerar 3000-6000 interações simuladas com respostas e classificação de erros.

#### Processo
1. **Carregamento de Dados**: Perfis, estudantes, questões, conceitos
2. **Configuração**: Definir 30-60 interações por estudante
3. **Geração de Interações**:
   - Selecionar questão aleatória
   - Calcular probabilidade de resposta correta (BKT)
   - Gerar resposta simulada
   - Classificar erro se houver
   - Atualizar domínio (mastery)
4. **Análise de Qualidade**: Acurácia, distribuição de erros
5. **Salvamento**: JSON com metadados

#### Cálculo de Probabilidade (BKT)
```
P(correct) = mastery + (1 - mastery) × guess - mastery × slip
```

#### Tipos de Erro
- `misconception`: Conceito errado
- `careless`: Erro por descuido
- `slip`: Erro por distração
- `incomplete`: Resposta incompleta
- `misunderstanding`: Entendimento errado

#### Saída
- **Arquivo**: `data/output/interactions.json`
- **Conteúdo**:
  ```json
  {
    "metadata": {
      "total_interactions": 5000,
      "total_students": 100,
      "avg_interactions_per_student": 50,
      "accuracy": 0.62,
      "quality_metrics": { ... }
    },
    "interactions": [
      {
        "interaction_id": "int_000000",
        "student_id": "student_0000",
        "question_id": "q_001",
        "is_correct": true,
        "error_type": null,
        "mastery_before": 0.45,
        "mastery_after": 0.48,
        "time_spent_seconds": 45
      },
      ...
    ]
  }
  ```

#### Tempo de Execução
~30-60 segundos

---

### 3.4 Etapa 4: Análise e Métricas

**Arquivo**: `04_analise_metricas.ipynb`

#### Objetivo
Validar realismo dos dados e responder às perguntas obrigatórias.

#### Processo
1. **Carregamento de Todos os Dados**: Perfis, estudantes, interações
2. **Validação de Realismo**:
   - Acurácia realista (30-90%)
   - Padrão de aprendizado monotônico
   - Correlação entre perfis e desempenho
   - Variação de tempo
3. **Análise de Fatores**: Calcular importância de cada fator
4. **Respostas Obrigatórias**: Responder 5 perguntas da atividade
5. **Compilação de Relatório**: Gerar relatório final

#### Validações Implementadas
- ✓ Acurácia realista
- ✓ Padrão de aprendizado crescente
- ✓ Diferença entre perfis
- ✓ Variação de tempo
- ✓ Distribuição de erros

#### Saída
- **Arquivo**: `data/output/analysis_report.json`
- **Conteúdo**:
  ```json
  {
    "metadata": { ... },
    "realism_validation": { ... },
    "learning_factors_analysis": { ... },
    "mandatory_questions_answers": { ... },
    "summary": {
      "overall_quality": "ALTA",
      "data_ready_for_training": true
    }
  }
  ```

#### Tempo de Execução
~10-20 segundos

---

## 4. Como Executar

### 4.1 Pré-requisitos

```bash
# Instalar dependências
pip install -r requirements.txt
```

### 4.2 Executar Pipeline Completo

Execute os notebooks na ordem:

```bash
# 1. Gerar perfis cognitivos
jupyter notebook 01_geracao_perfis.ipynb

# 2. Gerar estudantes sintéticos
jupyter notebook 02_geracao_estudantes.ipynb

# 3. Gerar dados de interação
jupyter notebook 03_geracao_interacoes.ipynb

# 4. Análise e métricas
jupyter notebook 04_analise_metricas.ipynb
```

### 4.3 Tempo Total

- Etapa 1: ~10s
- Etapa 2: ~5s
- Etapa 3: ~45s
- Etapa 4: ~15s
- **Total**: ~75 segundos (~1 minuto 15 segundos)

---

## 5. Arquivos de Entrada

### 5.1 concepts_graph.json
- **Fonte**: Grafo de conceitos do Linux
- **Uso**: Referência para conceitos nas interações
- **Formato**: Lista de conceitos com metadados

### 5.2 questions_graph.json
- **Fonte**: Grafo de questões gerado
- **Uso**: Seleção aleatória de questões para interações
- **Formato**: Lista de questões com tipo e dificuldade

---

## 6. Arquivos de Saída

### 6.1 profiles.json
- **Tamanho**: ~5 KB
- **Conteúdo**: 7 perfis com 9 parâmetros cada
- **Uso**: Entrada para Etapa 2

### 6.2 students.json
- **Tamanho**: ~50 KB
- **Conteúdo**: 100 estudantes com parâmetros individualizados
- **Uso**: Entrada para Etapa 3

### 6.3 interactions.json
- **Tamanho**: ~2-3 MB
- **Conteúdo**: 3000-6000 interações com respostas
- **Uso**: Dados para treinamento de SINKT

### 6.4 analysis_report.json
- **Tamanho**: ~100-200 KB
- **Conteúdo**: Análise completa e respostas obrigatórias
- **Uso**: Documentação e validação

---

## 7. Parâmetros Configuráveis

### 7.1 Etapa 2: Número de Estudantes
```python
NUM_STUDENTS = 100  # Pode aumentar para 200, 500, etc.
```

### 7.2 Etapa 3: Interações por Estudante
```python
MIN_INTERACTIONS_PER_STUDENT = 30
MAX_INTERACTIONS_PER_STUDENT = 60
```

### 7.3 Seed para Reprodutibilidade
```python
SEED = 42  # Mudar para obter diferentes amostras
```

---

## 8. Reprodutibilidade

O pipeline é **100% reprodutível**:

1. **Seed fixa**: Todos os números aleatórios usam seed=42
2. **Processo determinístico**: Mesmas entradas → mesmas saídas
3. **Auditabilidade**: Cada etapa registra metadados

Para reproduzir exatamente os mesmos resultados:
```bash
# Executar novamente com mesmos parâmetros
jupyter notebook 01_geracao_perfis.ipynb
jupyter notebook 02_geracao_estudantes.ipynb
jupyter notebook 03_geracao_interacoes.ipynb
jupyter notebook 04_analise_metricas.ipynb
```

---

## 9. Próximos Passos

### 9.1 Treinamento de SINKT
```python
from sinkt import SINKTModel

# Carregar dados
with open('data/output/interactions.json') as f:
    interactions = json.load(f)

# Treinar modelo
model = SINKTModel()
model.fit(interactions)
```

### 9.2 Validação com Dados Reais
1. Coletar dados reais de estudantes
2. Comparar distribuições
3. Calibrar parâmetros
4. Retreinar modelo

### 9.3 Expansão para Novos Domínios
1. Criar novos grafos de conceitos
2. Gerar novos perfis específicos do domínio
3. Repetir pipeline
4. Validar com dados reais

---

## 10. Troubleshooting

### Problema: "FileNotFoundError: concepts_graph.json"
**Solução**: Verificar se `data/json/concepts_graph.json` existe

### Problema: "MemoryError"
**Solução**: Reduzir `NUM_STUDENTS` ou `MAX_INTERACTIONS_PER_STUDENT`

### Problema: Resultados diferentes a cada execução
**Solução**: Verificar se `SEED` está definido corretamente

---

## 11. Referências

- **BKT**: Corbett & Anderson (1994)
- **Bloom's Taxonomy**: Bloom (1956)
- **Working Memory**: Swanson & Beebe-Frankenberger (2004)

---

**Documento Preparado Por**: Sistema SINKT  
**Data**: 14 de Dezembro de 2025  
**Versão**: 1.0.0
