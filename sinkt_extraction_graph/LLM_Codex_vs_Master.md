# Guia Definitivo: Pipeline de Engenharia de Conhecimento SINKT (Codex vs Master)

Este documento detalha o funcionamento técnico, os prompts literais e a lógica de execução dos dois pipelines.

## Resumo Executivo

**Ambas as versões compartilham 75% do pipeline (Fases 1-3). A diferença está na Fase 4:**

| Aspecto | CODEX | MASTER |
|---------|-------|--------|
| **Arquitetura Fase 4** | Multi-Agente Real (LangGraph) | Mega-Prompt (Role-Playing) |
| **Número de Agentes** | 4 agentes sequenciais | 8 personas simuladas |
| **Calls de API/Aresta** | 4 chamadas separadas | 1 chamada (batch de 15) |
| **Resultado Final** | 260 arestas (alta densidade) | 174 arestas (alta precisão) |
| **Custo** | ~60x mais caro | Mais eficiente |
| **Auditabilidade** | Log detalhado por agente | Debate interno opaco |

## Diagrama de Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    FASE 1-2: PIPELINE COMUM                      │
│                     (Idêntico em ambos)                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Extração → gpt-4o-mini (26 capítulos paralelos)              │
│    ↓ ~360 conceitos brutos                                       │
│ 2. Indução Ontologia → gpt-4o (taxonomia canônica)              │
│    ↓ ~254 conceitos limpos                                       │
│ 3. Extração Relações → gpt-4o-mini (capítulo a capítulo)        │
│    ↓ ~254 relações iniciais                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  FASE 3: DENSIFICAÇÃO HÍBRIDA                    │
│                     (Idêntico em ambos)                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Cleaner → gpt-4o-mini (remove ruídos)                        │
│ 2. Architect → text-embedding-3-small + gpt-4o-mini             │
│    (similaridade vetorial + validação semântica)                 │
│ 3. Teacher → gpt-4o-mini (promove PREREQUISITE)                 │
│    ↓ +12-18 novas arestas                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        │                                           │
┌───────▼──────────┐                    ┌───────────▼──────────┐
│  CODEX (Swarm)   │                    │  MASTER (Oracle)     │
│  FASE 4          │                    │  FASE 4              │
├──────────────────┤                    ├──────────────────────┤
│ LangGraph:       │                    │ Mega-Prompt:         │
│ • Cleaner        │                    │ • 8 Personas         │
│ • Expert         │                    │   Simuladas          │
│ • Analyst        │                    │ • 1 Call/15 arestas  │
│ • Judge          │                    │                      │
│                  │                    │                      │
│ 4 calls/aresta   │                    │ Batch Processing     │
│ ~252 candidatos  │                    │ ~261 candidatos      │
│ ↓                │                    │ ↓                    │
│ 260 arestas ✓    │                    │ 174 arestas ✓        │
└──────────────────┘                    └──────────────────────┘
```

---

## Fase 1 e 2: O Pipeline Comum (Alicerce)
*(Idêntico em ambas as versões)*

### 1. Extração de Conceitos (Concept Extraction)
*   **Modelo:** `gpt-4o-mini` (ChatOpenAI)
*   **Execução:** Paralela (3 workers) em todos os 26 capítulos do livro
*   **Prompt de Sistema:**
    ```text
    Você é um Especialista em Knowledge Tracing e Engenharia de Dados.
    Sua tarefa é extrair conceitos técnicos (Knowledge Components) de material didático sobre Linux.
    ### DIRETRIZES DE FILTRAGEM (NEGATIVE CONSTRAINTS):
    Para reduzir ruído, você deve **IGNORAR** ativamente:
    1. Variáveis e Placeholders ($VAR, <param>).
    2. Metadados Editoriais (Capítulo X, Página Y).
    3. Termos Genéricos (apenas termos técnicos válidos).
    ```
*   **Resultado:** ~360 conceitos brutos extraídos (Master) / ~333 (Codex)

### 2. Indução de Ontologia (Ontology Induction)
*   **Modelo:** `gpt-4o` (ChatOpenAI)
*   **Função:** Criar taxonomia canônica a partir dos tipos brutos extraídos
*   **Prompt:**
    ```text
    Analise os tipos brutos e mapeie para categorias mestras:
    COMANDO, SISTEMA_ARQUIVOS, REDE, CONCEITO_TEORICO, FERRAMENTA, HARDWARE, SHELL_SCRIPT, NOISE
    Mapeie ruídos (metadados, OCR) para categoria especial 'NOISE'.
    ```
*   **Resultado:** ~140 tipos brutos → 7 categorias canônicas + NOISE

### 3. Normalização e Consolidação
*   **Processo:** Aplicar mapa ontológico, filtrar NOISE, deduplicar por nome
*   **Resultado:** ~254 conceitos únicos consolidados (Master) / ~216 (Codex)

### 4. Extração de Relações (Relation Extraction)
*   **Modelo:** `gpt-4o-mini` (ChatOpenAI)
*   **Execução:** Paralela (3 workers) capítulo a capítulo
*   **Prompt de Usuário:**
    ```text
    Analise o texto do Capítulo {chapter_id} e a lista de conceitos presentes nele.
    Lista de Conceitos Válidos (Nós): {concept_list}
    Identifique as relações semânticas (IS_A, PART_OF, USE, PREREQUISITE, RELATED_TO)
    explícitas ou implícitas entre esses conceitos.
    ```
*   **Resultado:** ~254 relações extraídas (Master) / ~212 (Codex)

---

## A Bifurcação: Estratégias de Validação

Aqui detalhamos a "caixa preta" de cada abordagem.

### CODEX: The Council Swarm (Busca Ativa Multi-Agente)

O Codex utiliza o **LangGraph** para orquestrar agentes autônomos que votam em cada aresta candidata.

#### Fase 3: Densificação Híbrida (3 Agentes)

**Pipeline:**
1. **The Cleaner** → 2. **The Architect (Híbrido)** → 3. **The Teacher**

##### Agente 1: The Cleaner (Triagem Rápida)
*   **Modelo:** `gpt-4o-mini` (via get_model("gpt-4o-mini")) (ChatOpenAI, llm_mini)
*   **Função:** Remover conceitos-ruído antes de gerar embeddings
*   **Execução:** Batches de 150 conceitos
*   **Resultado:** Remove ~17-28 ruídos (variáveis soltas, erros OCR)

##### Agente 2: The Architect (Arquiteto Híbrido)
**Parte 1 - Scout (Matemática Pura):**
*   **Modelo:** `text-embedding-3-small` (OpenAIEmbeddings, embeddings_model) (OpenAI Embeddings)
    *   **Função:** Gerar embeddings e calcular similaridade de cosseno
    *   **Threshold:** 0.82 (permissivo)
    *   **Top-K:** 8 vizinhos mais similares por nó
    *   **Resultado:** ~14-26 candidatos matemáticos
*   **Parte 2 - Validator (Validação Semântica):**
*   **Modelo:** `gpt-4o-mini` (ChatOpenAI, llm_mini)
    *   **Função:** Validar semanticamente os candidatos
    *   **Batches:** 20 pares por chamada
    *   **Decisão:** RELATED_TO, USE ou SKIP
    *   **Resultado:** ~12-18 conexões validadas

##### Agente 3: The Teacher (Pedagogo)
*   **Modelo:** `gpt-4o-mini` (ChatOpenAI, llm_mini)
*   **Função:** Promover relações para PREREQUISITE quando há dependência de aprendizado
*   **Batches:** 50 relações
*   **Resultado:** ~2-5 relações promovidas para PREREQUISITE

#### Fase 4: Validação Final Multi-Agente (LangGraph - 4 Agentes)

**Fluxo do LangGraph:**
`Cleaner` → `Expert` → `Analyst` → `Judge`

**Geração de Candidatos (Scout & Bridge):**
*   **Scout:** Similaridade > 0.75 (Top 350 candidatos)
*   **Bridge (Anti-Ilha):** Conceitos de capítulos distantes (>3 caps) com similaridade > 0.70 (Top 150)
*   **Total:** ~252-500 candidatos para validação

##### Agente 1: The Cleaner (O Porteiro)
*   **Modelo:** `gpt-4o-mini` (via get_model("gpt-4o-mini")) (ChatOpenAI, llm_mini)
*   **Função:** Triagem rápida - eliminar lixo óbvio antes dos modelos caros
*   **Execução:** Primeira etapa do fluxo (early rejection)
*   **Prompt:**
    ```text
    Você é o CLEANER do grafo de conhecimento.
    Analise a aresta: {source} ({source_type}) -> {target} ({target_type}) [Score: {score}]
    
    CRITÉRIOS DE ELIMINAÇÃO IMEDIATA (Vote REJECT):
    1. Alucinações (conceitos inexistentes no contexto Linux)
    2. Tipos Errados (variáveis soltas conectadas a conceitos teóricos)
    3. Meta-dados (artefatos do livro: Figura, Tabela, Página)
    
    Se minimamente plausível, vote ABSTAIN.
    ```
*   **Decisão:** REJECT ou ABSTAIN
*   **Otimização:** Se REJECT, pula Expert e Analyst (economia de tokens)

##### Agente 2: The Expert (Validador Técnico e Pedagógico)
*   **Modelo:** `gpt-4o` (via get_model("gpt-4o"))
*   **Função:** Validação técnica e pedagógica profunda
*   **Prompt:**
    ```text
    Você é o ESPECIALISTA SÊNIOR (Engenheiro Linux + Pedagogo).
    Analise: {source} -> {target}
    
    MISSÃO 1 - Validação Técnica:
    - A relação é tecnicamente verdadeira?
    
    MISSÃO 2 - Validação Pedagógica:
    - Aprender A desbloqueia B? → MODIFY: PREREQUISITE
    - A é ferramenta de B? → MODIFY: USE
    - A compõe B? → MODIFY: PART_OF
    - Apenas relacionado? → APPROVE: RELATED_TO
    ```
*   **Decisão:** APPROVE, REJECT, MODIFY (com tipo sugerido)

##### Agente 3: The Analyst (Arquiteto Estrutural)
*   **Modelo:** `gpt-4o` (via get_model("gpt-4o"))
*   **Função:** Consistência estrutural e ontológica
*   **Prompt:**
    ```text
    Você é o ANALISTA ESTRUTURAL.
    Analise: {source} ({source_type}) -> {target} ({target_type})
    
    CHECAGENS:
    1. Hierarquia de Tipos: 'Conceito Abstrato' não pode ser PART_OF 'Comando'
    2. Topologia: Direção da seta faz sentido? (Geral → Específico)
    3. Prevenção de Ciclos: Relação cria ciclo lógico?
    ```
*   **Decisão:** APPROVE ou REJECT

##### Agente 4: The Judge (Decisor Final)
*   **Modelo:** `gpt-4o` (via get_model("gpt-4o"))
*   **Função:** Sintetizar votos e emitir veredito final
*   **Input:** Dossiê completo com votos de Cleaner, Expert e Analyst
*   **Prompt:**
    ```text
    Você é o JUIZ SUPREMO do grafo SINKT.
    Decida: {source} -> {target}
    
    VOTOS DO CONSELHO:
    {votes}
    
    REGRAS:
    1. Veto Técnico: Se Expert ou Cleaner rejeitou → DISCARD
    2. Tipificação: Priorize tipo sugerido pelo Expert
    3. Segurança: Na dúvida → DISCARD
    ```
*   **Output:** KEEP ou DISCARD + tipo final + justificativa
*   **Resultado:** ~53 arestas aprovadas de ~252 candidatos

**📋 Modelos Declarados no Código:**
```python
MODELS = {
    "scout_embed": OpenAIEmbeddings(model="text-embedding-3-small"),
    "cleaner": get_model("gpt-4o-mini"),
    "expert": get_model("gpt-4o"),
    "analyst": get_model("gpt-4o"),
    "judge": get_model("gpt-4o"),
}
```

---

### MASTER: The SINKT Oracle (Auditoria Unificada)

O Master não usa múltiplos agentes chamando API separadamente. Ele usa um **Mega-Prompt (Role-Playing)** onde uma única chamada simula uma mesa redonda completa.

#### Fase 3: Densificação Híbrida (3 Agentes - Idêntico ao Codex)

**Pipeline:** Cleaner → Architect (Embeddings + Validator) → Teacher

*Mesma estrutura do Codex, com pequenas diferenças nos resultados:*
*   **Cleaner:** Remove ~28 ruídos (vs ~17 no Codex)
*   **Architect:** ~14 candidatos matemáticos → ~12 validados
*   **Teacher:** ~2 promovidos para PREREQUISITE
*   **Resultado:** 226 nós, 220 arestas (densidade: 0.00433)

#### Fase 4: Validação Final - O Oracle (Mesa Redonda Virtual)

*   **Modelo Declarado:** `gpt-5.1` (ChatOpenAI, llm_judge)
*   **Processamento:** Batches de 15 arestas por chamada
*   **Arquitetura:** Mega-Prompt simulando 8 personas em debate interno

**📋 Código:**
```python
llm_judge = ChatOpenAI(model="gpt-5.1", temperature=0)
```

##### As 8 Personas da Mesa Redonda:

1.  **Professor (Pedagogo):** Foca na Causalidade Pedagógica
    *   "Aprender A desbloqueia B?"
    *   Valida dependências de aprendizado

2.  **Engenheiro (Técnico):** Foca na Verdade Técnica
    *   "'ls' realmente lista arquivos?"
    *   Valida precisão factual Linux

3.  **Otimizador (Anti-Redundância):** Caça Duplicatas
    *   "Se A→B e B→C, precisamos de A→C?"
    *   Remove transitividades desnecessárias

4.  **Cético (Anti-Alucinação):** Caça Conceitos Falsos
    *   "'Linux' é um 'Comando'? Não!"
    *   Detecta erros de extração

5.  **Topólogo (Protetor de DAG):** Evita Ciclos
    *   "A depende de B, B não pode depender de A"
    *   Garante hierarquia Geral → Específico

6.  **Terminologista (Padronizador):** Unifica Tipos
    *   "Use PREREQUISITE apenas para bloqueios de aprendizado"
    *   Aplica taxonomia canônica

7.  **Reparador (Salvacionista):** Tenta Corrigir
    *   "Direção errada? Inverta!"
    *   "Tipo fraco? Fortaleça!"
    *   Propõe REFACTOR em vez de DISCARD

8.  **JUIZ (Decisor):** Sintetiza e Bate o Martelo
    *   Pondera votos das 7 personas
    *   Emite veredito final

##### Regras de Decisão do Oracle:

*   **KEEP:** Tecnicamente verdadeira + pedagogicamente útil + topologicamente segura
*   **REFACTOR:**
    *   Erro de Direção: "Shell PART_OF Bash" → Inverter para "Bash IS_A Shell"
    *   Erro de Tipo: "ls PREREQUISITE Terminal" → Mudar para "Terminal USE ls"
*   **DISCARD:**
    *   Alucinações (fatos falsos)
    *   Conexões genéricas ("Linux RELATED_TO Computador")
    *   Ciclos óbvios

##### Tipos Canônicos Permitidos:
1.  **PREREQUISITE:** Dependência de aprendizado (A antes de B)
2.  **PART_OF:** Composição (A é componente de B)
3.  **IS_A:** Taxonomia (A é tipo de B)
4.  **USE:** Funcional (A utiliza B)
5.  **RELATED_TO:** Associação genérica (último recurso)

##### Resultado da Validação:
*   **Input:** 261 relações para auditar
*   **Aprovadas:** 208 (KEEP + REFACTOR)
*   **Descartadas:** 38
*   **Refatoradas:** 134 (mudança de tipo ou direção)
*   **Output Final:** 226 nós, 174 arestas (densidade: 0.00342)

---

## Comparativo Técnico Final

Esta tabela resume os resultados obtidos na última execução de cada pipeline.

| Métrica / Recurso | **CODEX (Swarm)** | **MASTER (Oracle)** | **Análise** |
| :--- | :--- | :--- | :--- |
| **Pipeline Completo** | 4 Fases (Extraction → Ontology → Relations → Densification → Multi-Agent Council) | 4 Fases (Extraction → Ontology → Relations → Densification → Oracle Audit) | Estrutura idêntica, diferença na Fase 4. |
| **Fase 1-2 (Comum)** | gpt-4o-mini (Extraction) + gpt-4o (Ontology) | gpt-4o-mini (Extraction) + gpt-4o (Ontology) | Idêntico em ambas versões. |
| **Fase 3 (Densificação)** | 3 Agentes: Cleaner + Architect (Embeddings + gpt-4o-mini) + Teacher | 3 Agentes: Cleaner + Architect (Embeddings + gpt-4o-mini) + Teacher | Idêntico em ambas versões. |
| **Fase 4 (Validação)** | **LangGraph Multi-Agent:** 4 agentes sequenciais (Cleaner → Expert → Analyst → Judge) | **Mega-Prompt Oracle:** 8 personas simuladas em 1 chamada | **Diferença-chave:** Codex = 4 calls/aresta; Master = 1 call/15 arestas. |
| **Total de Nós** | **216** | **226** | Master manteve mais nós (Cleaner menos agressivo). |
| **Total de Arestas** | **260** 📈 | **174** 📉 | Codex expandiu (+49%) vs Master reduziu (-21%). |
| **Densidade do Grafo** | **0.0056** (Alta) | **0.0034** (Baixa) | Codex oferece mais caminhos para Knowledge Tracing. |
| **Nós Órfãos** | **0** (Zero) | **0** (Removidos) | Ambos resolveram o problema de "ilhas". |
| **Ciclos (Loops)** | Não medido | **19** | Master reportou ciclos residuais. |
| **Custo Computacional** | 🔴 **Alto** (4 LLM calls/aresta + embeddings) | 🟢 **Médio** (1 LLM call/15 arestas + embeddings) | Master é ~60x mais eficiente em calls de API. |
| **Granularidade de Debug** | 🟢 **Fina** (Log por agente, voto individual) | 🔴 **Grossa** (Debate interno opaco) | Codex permite auditoria detalhada. |
| **Filosofia** | **Recall** (Descoberta) | **Precision** (Segurança) | Codex: explorar; Master: certificar. |
| **Modelos Declarados (Fase 4)** | gpt-4o-mini + gpt-4o | gpt-5.1 | Codex: 2 modelos; Master: 1 modelo |

### Conclusão e Recomendação

1.  **Ambiente de Produção (Alunos Reais):** Recomenda-se o grafo **MASTER**. Embora mais esparso, a garantia de que as relações são tecnicamente corretas evita que o aluno receba recomendações de estudo erradas ou confusas.
2.  **Ambiente de Pesquisa (Data Science):** Recomenda-se o grafo **CODEX**. A maior densidade permite testar algoritmos de GNN (Graph Neural Networks) com mais profundidade, mesmo que haja algum ruído.
