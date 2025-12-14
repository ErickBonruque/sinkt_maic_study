# 🎯 Resposta: Como os Agentes e LLMs Executam nas Arestas/Nós?

## Sua Pergunta Original

> "Os quatro agentes e o super prompt, ambos executam em todas as arestas ou em todos os nós? Ou eles acessam mais de um nó, como isso é feito?"

---

## ✅ Resposta Direta

### 1. **Unidade de Trabalho: ARESTAS, não nós isolados**

Tanto o **CODEX (4 agentes)** quanto o **MASTER (Oracle de 8 personas)** trabalham **aresta por aresta**.

- Cada decisão analisa um **par de nós**: `source` → `target`
- Os agentes **não processam nós isolados**
- A entrada de cada agente é sempre uma **relação candidata** (aresta)

### 2. **Eles Executam em TODAS as Arestas?**

**Não exatamente.** Eles executam em **arestas candidatas** geradas nas fases anteriores:

#### CODEX (Fase 4):
- **Input:** ~252 arestas candidatas (geradas por similaridade vetorial)
  - Scout: Top 350 pares com similaridade > 0.75
  - Bridge: Top 150 pares de capítulos distantes (>3 caps) com similaridade > 0.70
- **Processo:** Cada aresta passa pelo fluxo `Cleaner → Expert → Analyst → Judge`
- **Output:** ~53 arestas aprovadas (21% de aprovação)

#### MASTER (Fase 4):
- **Input:** ~261 arestas candidatas (relações da Fase 3)
- **Processo:** Batches de 15 arestas por chamada ao Oracle
- **Output:** ~208 arestas aprovadas (80% de aprovação, mas com 134 refatorações)

### 3. **Como Eles "Acessam" os Nós?**

Dentro de cada decisão sobre uma aresta `A → B`, os agentes recebem:

```json
{
  "source": "ls",
  "source_type": "COMANDO",
  "target": "Terminal",
  "target_type": "CONCEITO_TEORICO",
  "similarity_score": 0.87,
  "chapter_distance": 5
}
```

**Contexto fornecido:**
- ✅ Nome e tipo dos 2 nós envolvidos (source e target)
- ✅ Score de similaridade vetorial
- ✅ Distância entre capítulos de origem
- ❌ **NÃO** recebem vizinhança completa (outros nós conectados)
- ❌ **NÃO** recebem subgrafo local

**Decisão local:** A análise é **pontual** na aresta, não considera o grafo global.

---

## 📊 Comparação: CODEX vs MASTER

| Aspecto | CODEX (4 Agentes Reais) | MASTER (8 Personas Simuladas) |
|---------|-------------------------|-------------------------------|
| **Execução** | 4 chamadas de API sequenciais por aresta | 1 chamada de API para 15 arestas |
| **Unidade** | Aresta individual | Batch de arestas |
| **Contexto** | Par de nós (source, target) | Par de nós (source, target) |
| **Acesso a vizinhos?** | ❌ Não | ❌ Não |
| **Decisão** | Votação entre agentes (REJECT/APPROVE/MODIFY) | Debate simulado (KEEP/DISCARD/REFACTOR) |
| **Custo** | 4 calls × 252 arestas = **1.008 calls** | 261 arestas ÷ 15 = **~18 calls** |
| **Eficiência** | Baixa (60x mais caro) | Alta |
| **Auditabilidade** | Alta (log por agente) | Baixa (debate interno opaco) |

---

## 🔍 Exemplo Prático: Processamento de uma Aresta

### Entrada (Candidato):
```
"ls" (COMANDO) → "Terminal" (CONCEITO_TEORICO)
Similaridade: 0.87
```

### CODEX (Fluxo Sequencial):

1. **Cleaner (gpt-4o-mini):**
   - Análise: "Conceitos válidos? Sim. Não é metadado."
   - Voto: `ABSTAIN` (passa para o próximo)

2. **Expert (gpt-4o):**
   - Análise Técnica: "'ls' é executado no Terminal? Sim."
   - Análise Pedagógica: "Precisa entender Terminal para usar 'ls'? Sim."
   - Voto: `MODIFY → PREREQUISITE`

3. **Analyst (gpt-4o):**
   - Checagem Estrutural: "Direção correta? Sim (Terminal → ls)."
   - Checagem Ontológica: "Tipos compatíveis? Sim."
   - Voto: `APPROVE`

4. **Judge (gpt-4o):**
   - Síntese: "Expert sugeriu PREREQUISITE, Analyst aprovou."
   - Decisão: `KEEP como PREREQUISITE`

**Resultado:** Aresta aprovada como `Terminal → PREREQUISITE → ls`

---

### MASTER (Debate Simulado):

**Prompt único para o Oracle (batch de 15 arestas):**

```
Aresta 7/15: "ls" (COMANDO) → "Terminal" (CONCEITO_TEORICO)

[Debate Interno Simulado]
- Professor: "Entender Terminal é pré-requisito para usar 'ls'? Sim."
- Engenheiro: "Tecnicamente correto? Sim."
- Topólogo: "Cria ciclo? Não."
- Terminologista: "Tipo correto? PREREQUISITE."
- Juiz: "Veredito: KEEP como PREREQUISITE."
```

**Resultado:** Aresta aprovada como `Terminal → PREREQUISITE → ls`

---

## 🎓 Conclusão

### Respondendo suas perguntas:

1. **"Executam em todas as arestas ou nós?"**
   - ✅ Executam em **arestas candidatas** (não todas, apenas as geradas por similaridade)
   - ❌ **Não** executam em nós isolados

2. **"Eles acessam mais de um nó?"**
   - ✅ Sim, sempre **2 nós por vez** (source e target da aresta)
   - ❌ Não acessam vizinhança ou subgrafo completo

3. **"Como isso é feito?"**
   - **CODEX:** 4 agentes votam sequencialmente em cada aresta
   - **MASTER:** 1 agente simula 8 personas em batch de 15 arestas

### Diferença-Chave:

- **CODEX:** Processamento **individual** (1 aresta por vez, 4 calls)
- **MASTER:** Processamento **em lote** (15 arestas por call, 1 call)

Ambos tomam decisões **locais** (par de nós), sem contexto global do grafo.
