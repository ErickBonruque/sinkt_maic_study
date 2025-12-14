# SINKT - Simulação de Estudantes Sintéticos para Treinamento de Modelos de Knowledge Tracing

**Versão**: 2.0.0  
**Data**: 14 de Dezembro de 2025  
**Status**: ✅ Pronto para Execução

---

## 📋 Visão Geral

Este projeto implementa um **pipeline completo de geração de dados sintéticos** para treinar modelos de Knowledge Tracing em cenários de cold start. O pipeline SINKT gera:

- ✅ **7 perfis cognitivos** fundamentados em BKT (Bayesian Knowledge Tracing)
- ✅ **100 estudantes sintéticos** com variação individual realista
- ✅ **3000-6000 interações** com respostas simuladas e classificação de erros
- ✅ **Análise completa** com validação de realismo e respostas obrigatórias

---

## 🚀 Quick Start

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar Pipeline Completo
```bash
# Etapa 1: Gerar perfis cognitivos
jupyter notebook 01_geracao_perfis.ipynb

# Etapa 2: Gerar estudantes sintéticos
jupyter notebook 02_geracao_estudantes.ipynb

# Etapa 3: Gerar dados de interação
jupyter notebook 03_geracao_interacoes.ipynb

# Etapa 4: Análise e métricas
jupyter notebook 04_analise_metricas.ipynb
```

### 3. Tempo Total
⏱️ **~75 segundos** (1 minuto 15 segundos)

---

## 📁 Estrutura do Projeto

```
simulacao_estudantes/
├── 01_geracao_perfis.ipynb              # Etapa 1: Criar 7 perfis cognitivos
├── 02_geracao_estudantes.ipynb          # Etapa 2: Gerar 100 estudantes
├── 03_geracao_interacoes.ipynb          # Etapa 3: Gerar 3000-6000 interações
├── 04_analise_metricas.ipynb            # Etapa 4: Análise e validação
├── data/
│   ├── json/
│   │   ├── concepts_graph.json          # Grafo de conceitos (entrada)
│   │   └── questions_graph.json         # Grafo de questões (entrada)
│   └── output/
│       ├── profiles.json                # Perfis gerados
│       ├── students.json                # Estudantes gerados
│       ├── interactions.json            # Interações geradas
│       ├── analysis_report.json         # Relatório de análise
│       └── metrics_summary.json         # Resumo de métricas
├── docs/
│   ├── 01_justificativa_perfis.md       # Justificativa dos perfis (IMPORTANTE)
│   ├── 02_pipeline_sinkt.md             # Guia do pipeline
│   └── 03_respostas_obrigatorias.md     # Respostas às perguntas
├── requirements.txt                      # Dependências Python
└── README.md                             # Este arquivo
```

---

## 🎯 Etapas do Pipeline

### Etapa 1: Geração de Perfis Cognitivos
**Arquivo**: `01_geracao_perfis.ipynb`

Cria 7 perfis cognitivos com 9 parâmetros cada:

| Perfil | ID | Distribuição | Características |
|--------|----|----|---|
| Equilibrado | `balanced` | 25% | Habilidades balanceadas |
| Aprendiz Rápido | `quick_learner` | 15% | Alta capacidade, poucos erros |
| Cuidadoso | `careful` | 15% | Baixa taxa de erros, aprendizado gradual |
| Com Dificuldades | `struggling` | 15% | Baixo domínio, aprendizado lento |
| Pensador Lógico | `logical` | 15% | Excelente lógica, fraco em leitura |
| Intuitivo | `intuitive` | 10% | Boa leitura, fraco em lógica |
| Perfeccionista | `perfectionist` | 5% | Muito rigoroso, aprendizado profundo |

**Saída**: `data/output/profiles.json` (~5 KB)

---

### Etapa 2: Geração de Estudantes Sintéticos
**Arquivo**: `02_geracao_estudantes.ipynb`

Gera 100 estudantes com variação individual:

- ✓ 100 estudantes distribuídos entre 7 perfis
- ✓ Variação individual ±15% por parâmetro
- ✓ Reprodutibilidade com seed=42
- ✓ Validação de qualidade

**Saída**: `data/output/students.json` (~50 KB)

---

### Etapa 3: Geração de Dados de Interação
**Arquivo**: `03_geracao_interacoes.ipynb`

Gera 3000-6000 interações simuladas:

- ✓ 30-60 interações por estudante
- ✓ Respostas simuladas baseadas em BKT
- ✓ Classificação de erros (5 tipos)
- ✓ Atualização de domínio (mastery) ao longo do tempo

**Saída**: `data/output/interactions.json` (~2-3 MB)

---

### Etapa 4: Análise e Métricas
**Arquivo**: `04_analise_metricas.ipynb`

Valida realismo e responde perguntas obrigatórias:

- ✓ Validação de realismo dos dados
- ✓ Análise de fatores influenciadores
- ✓ Respostas às 5 perguntas obrigatórias
- ✓ Relatório completo

**Saída**: `data/output/analysis_report.json` (~100-200 KB)

---

## 📊 Parâmetros dos Perfis

Cada perfil é caracterizado por **9 parâmetros fundamentais**:

### Parâmetros BKT (Knowledge Tracing)
- **mastery_init_level**: Nível inicial de domínio (0-1)
- **learn_rate**: Taxa de aprendizagem (0-0.1)
- **slip**: Probabilidade de erro quando sabe (0-0.2)
- **guess**: Probabilidade de acerto quando não sabe (0-0.3)

### Parâmetros Cognitivos
- **logic_skill**: Habilidade lógica (0-1)
- **reading_skill**: Habilidade de leitura (0-1)
- **memory_capacity**: Capacidade de memória (0-1)
- **tech_familiarity**: Familiaridade com tecnologia (0-1)
- **learning_consistency**: Consistência de aprendizado (0-1)

---

## 📈 Estatísticas Esperadas

### Acurácia por Perfil
| Perfil | Acurácia Esperada |
|--------|---|
| Aprendiz Rápido | 75-85% |
| Perfeccionista | 80-85% |
| Equilibrado | 60-65% |
| Intuitivo | 60-65% |
| Pensador Lógico | 70-75% |
| Cuidadoso | 70-75% |
| Com Dificuldades | 35-45% |

### Tempo de Aprendizado
| Perfil | Interações para Convergência |
|--------|---|
| Aprendiz Rápido | 5-10 |
| Perfeccionista | 10-15 |
| Equilibrado | 15-20 |
| Cuidadoso | 15-20 |
| Pensador Lógico | 15-20 |
| Intuitivo | 15-20 |
| Com Dificuldades | 30-50 |

---

## 🔍 Validações Implementadas

### Validação de Realismo
- ✓ Acurácia realista (30-90%)
- ✓ Padrão de aprendizado monotônico (70%+ dos estudantes)
- ✓ Diferença entre perfis (correlação com desempenho)
- ✓ Variação de tempo (desvio padrão > 20s)

### Validação de Coerência
- ✓ `learn_rate` alto → `slip` baixo
- ✓ `logic_skill` alto → `guess` baixo
- ✓ `memory_capacity` alto → `learning_consistency` alto

### Validação de Integridade
- ✓ IDs únicos
- ✓ Referências válidas
- ✓ Parâmetros no range [0, 1]
- ✓ Campos obrigatórios preenchidos

---

## 📚 Documentação

### Documentos Inclusos
1. **01_justificativa_perfis.md** - Justificativa detalhada de cada perfil
2. **02_pipeline_sinkt.md** - Guia completo do pipeline
3. **03_respostas_obrigatorias.md** - Respostas às 5 perguntas obrigatórias

### Leitura Recomendada
1. Comece por: `docs/01_justificativa_perfis.md`
2. Depois: `docs/02_pipeline_sinkt.md`
3. Finalmente: `docs/03_respostas_obrigatorias.md`

---

## 🔧 Configurações Personalizáveis

### Etapa 1: Perfis
```python
# Editar profiles_data para adicionar/modificar perfis
profiles_data = [
    {
        "id": "seu_perfil",
        "nome": "Seu Perfil",
        "mastery_init_level": 0.50,
        ...
    }
]
```

### Etapa 2: Estudantes
```python
NUM_STUDENTS = 100  # Aumentar/diminuir número de estudantes
INDIVIDUAL_VARIATION = 0.15  # Ajustar variação (±15%)
SEED = 42  # Mudar para diferentes amostras
```

### Etapa 3: Interações
```python
MIN_INTERACTIONS_PER_STUDENT = 30
MAX_INTERACTIONS_PER_STUDENT = 60
```

---

## 💾 Arquivos de Saída

### profiles.json
```json
{
  "metadata": {
    "num_profiles": 7,
    "parameters_count": 9,
    "model": "BKT + Cognitive Factors"
  },
  "profiles": {
    "balanced": { ... },
    ...
  }
}
```

### students.json
```json
{
  "metadata": {
    "num_students": 100,
    "generation_seed": 42,
    "quality_metrics": { ... }
  },
  "students": {
    "student_0000": { ... },
    ...
  }
}
```

### interactions.json
```json
{
  "metadata": {
    "total_interactions": 5000,
    "accuracy": 0.62,
    "quality_metrics": { ... }
  },
  "interactions": [
    {
      "interaction_id": "int_000000",
      "student_id": "student_0000",
      "is_correct": true,
      "error_type": null,
      "mastery_after": 0.48,
      ...
    }
  ]
}
```

---

## 🎓 Respostas às Perguntas Obrigatórias

### ❓ P1: Como garantir que os perfis criados representam comportamentos cognitivos realistas?

**R**: Perfis baseados em BKT (modelo clássico de Knowledge Tracing), com validação de coerência entre parâmetros e sem fatores demográficos. Cada perfil tem 9 parâmetros fundamentados em teoria educacional.

### ❓ P2: Quais fatores realmente influenciam o aprendizado?

**R**: Análise de correlação mostra os fatores mais importantes. Típicamente: `learn_rate`, `logic_skill`, `memory_capacity` são os mais influentes.

### ❓ P3: Os fatores demográficos devem ser modelados?

**R**: **NÃO**. Fatores demográficos (idade, gênero, classe social) podem introduzir viés e discriminação. Modelo deve ser justo e neutro.

### ❓ P4: Como garantir boa acurácia sem dados reais?

**R**: Dados sintéticos coerentes com modelos teóricos validados, validação de realismo, e calibração futura com dados reais.

### ❓ P5: Como validar se os dados sintéticos parecem humanos?

**R**: Múltiplas validações: acurácia realista, padrão de aprendizado monotônico, diferença entre perfis, variação de tempo.

---

## 🚦 Status do Projeto

| Componente | Status |
|-----------|--------|
| Perfis Cognitivos | ✅ Completo |
| Estudantes Sintéticos | ✅ Completo |
| Geração de Interações | ✅ Completo |
| Análise e Métricas | ✅ Completo |
| Documentação | ✅ Completo |
| Validação | ✅ Completo |

---

## 📋 Checklist de Execução

- [ ] Instalar dependências: `pip install -r requirements.txt`
- [ ] Executar Notebook 1: `01_geracao_perfis.ipynb`
- [ ] Executar Notebook 2: `02_geracao_estudantes.ipynb`
- [ ] Executar Notebook 3: `03_geracao_interacoes.ipynb`
- [ ] Executar Notebook 4: `04_analise_metricas.ipynb`
- [ ] Verificar arquivos em `data/output/`
- [ ] Ler documentação em `docs/`
- [ ] Validar relatório em `analysis_report.json`

---

## 🔗 Próximos Passos

1. **Treinamento de SINKT**: Usar `interactions.json` para treinar modelo
2. **Validação com Dados Reais**: Comparar com dados reais quando disponíveis
3. **Calibração**: Ajustar parâmetros baseado em feedback
4. **Expansão**: Aplicar a novos domínios

---

## 📖 Referências

- **Corbett, A. T., & Anderson, J. R. (1994)**. Knowledge Tracing: Modeling the Acquisition of Procedural Knowledge.
- **Bloom, B. S. (1956)**. Taxonomy of Educational Objectives.
- **Swanson, H. L., & Beebe-Frankenberger, M. (2004)**. The Relationship Between Working Memory and Mathematical Problem Solving.

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação em `docs/`
2. Verifique o arquivo de análise: `data/output/analysis_report.json`
3. Revise os notebooks para entender o processo

---

## 📄 Licença

MIT License - Veja LICENSE para detalhes

---

**Projeto**: SINKT - Simulação de Estudantes Sintéticos  
**Versão**: 2.0.0  
**Data**: 14 de Dezembro de 2025  
**Status**: ✅ Pronto para Execução e Uso
