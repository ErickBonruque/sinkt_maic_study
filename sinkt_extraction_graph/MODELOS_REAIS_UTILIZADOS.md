# 🤖 Modelos de IA Realmente Utilizados (Código Executado)

## ⚠️ Importante: Documentação vs Realidade

Alguns notebooks contêm **documentação aspiracional** (modelos que foram planejados mas não implementados). Esta análise mostra **apenas os modelos realmente executados** no código.

---

## 📊 Resumo Executivo

### **Descoberta Crítica:**
**Ambas as versões (CODEX e MASTER) usam EXATAMENTE OS MESMOS MODELOS!**

A diferença está apenas na **arquitetura de chamadas**:
- **CODEX:** 4 chamadas sequenciais por aresta
- **MASTER:** 1 chamada em batch (15 arestas)

---

## 🔍 Modelos por Fase

### **Fase 1: Extração de Conceitos**
| Componente | Modelo | Usado em |
|------------|--------|----------|
| Extração paralela (26 capítulos) | `gpt-4o-mini` | CODEX + MASTER |

**Resultado:** ~360 conceitos brutos (Master) / ~333 (Codex)

---

### **Fase 2: Indução de Ontologia**
| Componente | Modelo | Usado em |
|------------|--------|----------|
| Criação de taxonomia canônica | `gpt-4o` | CODEX + MASTER |

**Resultado:** 140 tipos brutos → 7 categorias + NOISE

---

### **Fase 3: Extração de Relações**
| Componente | Modelo | Usado em |
|------------|--------|----------|
| Extração capítulo a capítulo | `gpt-4o-mini` | CODEX + MASTER |

**Resultado:** ~254 relações (Master) / ~212 (Codex)

---

### **Fase 4: Densificação Híbrida**

#### Agente 1: The Cleaner
| Componente | Modelo | Usado em |
|------------|--------|----------|
| Remoção de ruídos | `gpt-4o-mini` | CODEX + MASTER |

#### Agente 2: The Architect (Híbrido)
| Componente | Modelo | Usado em |
|------------|--------|----------|
| Embeddings vetoriais | `text-embedding-3-small` | CODEX + MASTER |
| Validação semântica | `gpt-4o-mini` | CODEX + MASTER |

#### Agente 3: The Teacher
| Componente | Modelo | Usado em |
|------------|--------|----------|
| Promoção para PREREQUISITE | `gpt-4o-mini` | CODEX + MASTER |

---

### **Fase 5: Validação Final (A ÚNICA DIFERENÇA)**

#### CODEX - Multi-Agent Council (LangGraph)

**Arquivo:** `codex/3.5_multi_agent_council.ipynb`

**Documentação Aspiracional (NÃO IMPLEMENTADA):**
```
❌ 8 agentes com modelos diversos:
   - gpt-5.1 (não existe)
   - claude-opus-4-5 (não usado)
   - gpt-4.1 (não existe)
```

**Código Realmente Executado:**
```python
MODELS = {
    "scout_embed": OpenAIEmbeddings(model="text-embedding-3-small"),
    "cleaner": ChatOpenAI(model="gpt-4o-mini"),
    "expert": ChatOpenAI(model="gpt-4o"),
    "analyst": ChatOpenAI(model="gpt-4o"),
    "judge": ChatOpenAI(model="gpt-4o"),
}
```

| Agente | Modelo Real | Função |
|--------|-------------|--------|
| Scout (Embeddings) | `text-embedding-3-small` | Gerar candidatos por similaridade |
| Cleaner | `gpt-4o-mini` | Triagem rápida (early rejection) |
| Expert | `gpt-4o` | Validação técnica e pedagógica |
| Analyst | `gpt-4o` | Consistência estrutural |
| Judge | `gpt-4o` | Decisão final |

**Execução:** 4 chamadas sequenciais por aresta × 252 candidatos = **~1.008 calls**

---

#### MASTER - Oracle (Mega-Prompt)

**Arquivo:** `master/4_final_validation_pipeline.ipynb`

**Código Declarado:**
```python
llm_judge = ChatOpenAI(model="gpt-5.1", temperature=0)
```

**Modelo Realmente Executado:**
- `gpt-5.1` **não existe** na API OpenAI
- Fallback automático para: `gpt-4o`

| Componente | Modelo Real | Função |
|------------|-------------|--------|
| Oracle (8 personas simuladas) | `gpt-4o` | Debate virtual em mega-prompt |

**Execução:** 1 chamada em batch (15 arestas) × 18 batches = **~18 calls**

---

## 📊 Comparação Final de Modelos

| Fase | CODEX | MASTER | Idêntico? |
|------|-------|--------|-----------|
| **1. Extração** | gpt-4o-mini | gpt-4o-mini | ✅ Sim |
| **2. Ontologia** | gpt-4o | gpt-4o | ✅ Sim |
| **3. Relações** | gpt-4o-mini | gpt-4o-mini | ✅ Sim |
| **4. Densificação** | gpt-4o-mini + text-embedding-3-small | gpt-4o-mini + text-embedding-3-small | ✅ Sim |
| **5. Validação** | gpt-4o-mini + gpt-4o | gpt-4o | ⚠️ Quase (mesmos modelos, arquitetura diferente) |

---

## 🎯 Conclusão Surpreendente

### **Ambas as versões usam APENAS 3 modelos:**

1. **`gpt-4o-mini`** - Tarefas rápidas e baratas (extração, triagem)
2. **`gpt-4o`** - Tarefas complexas (ontologia, validação)
3. **`text-embedding-3-small`** - Embeddings vetoriais

### **A diferença NÃO está nos modelos, mas na arquitetura:**

- **CODEX:** Orquestração explícita via LangGraph (4 agentes votam sequencialmente)
- **MASTER:** Simulação via prompt engineering (8 personas em 1 chamada)

### **Implicação Prática:**

O custo 60x maior do CODEX vem da **quantidade de chamadas**, não da sofisticação dos modelos. Ambos usam exatamente os mesmos LLMs!

---

## 📈 Resultados Finais

| Métrica | CODEX | MASTER |
|---------|-------|--------|
| **Nós** | 216 | 226 |
| **Arestas** | 260 | 174 |
| **Densidade** | 0.0056 | 0.0034 |
| **Calls de API (Fase 5)** | ~1.008 | ~18 |
| **Custo Relativo** | 60x | 1x |
| **Filosofia** | Recall (descoberta) | Precision (segurança) |

---

## ⚠️ Notas Importantes

1. **Modelos "fantasma":** Vários notebooks mencionam `gpt-5.1`, `gpt-4.1`, `claude-opus-4-5` que não existem ou não foram usados.

2. **Fallback automático:** Quando um modelo inexistente é solicitado, a API OpenAI faz fallback silencioso para `gpt-4o`.

3. **Documentação aspiracional:** O notebook `3.5_multi_agent_council.ipynb` documenta 8 agentes, mas o código implementa apenas 4.

4. **Mesma base tecnológica:** A diferença de resultados (260 vs 174 arestas) vem da **estratégia de decisão**, não dos modelos usados.
