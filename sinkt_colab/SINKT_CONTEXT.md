# SINKT (Structure-Aware Inductive Knowledge Tracing) - AI Global Context

## 1. Identidade e Propósito
Este documento serve como a "memória central" e contexto técnico para uma IA assistente de desenvolvimento. O objetivo é permitir a implementação, refatoração e expansão do projeto **SINKT**, um sistema de Rastreamento de Conhecimento (Knowledge Tracing) focado em educação, especificamente programado para o domínio de Python (no estado atual), mas arquitetado para ser agnóstico ao domínio.

**Sua Missão:** Auxiliar na transição de um protótipo em Notebook (Jupyter) para um microserviço robusto (API REST), mantendo a fidelidade teórica ao artigo original do SINKT e respeitando a implementação prática atual.

---

## 2. Fundamentação Teórica (Resumo do Artigo SINKT)

O SINKT (*Structure-Aware Inductive Knowledge Tracing*) resolve dois problemas principais do Knowledge Tracing tradicional (como DKT ou BKT):
1.  **Cold Start/Indutivo:** Modelos tradicionais usam IDs fixos. O SINKT usa **conteúdo semântico** (texto das questões/conceitos) e **grafos**, permitindo prever o desempenho em questões *novas* (que nunca foram vistas no treino).
2.  **Estrutura do Conhecimento:** Incorpora explicitamente as relações entre conceitos (pré-requisitos, similaridade) através de um grafo heterogêneo.

### Arquitetura Teórica (Paper):
1.  **Gerador de Grafo (LLM):** Usa LLMs para criar arestas *Conceito-Conceito*, *Conceito-Questão* e *Questão-Conceito*.
2.  **Textual Information Encoder:** Usa modelos como BERT ou Vicuna para gerar embeddings semânticos dos textos.
3.  **Structural Information Encoder (SIEnc):** Usa Graph Attention Networks (GAT) para propagar informação no grafo.
4.  **Student State Encoder (GRU):** Uma rede neural recorrente que processa a sequência temporal de tentativas do aluno.

---

## 3. Estado Atual da Implementação (Codebase v2.0)

Atualmente, o projeto é um protótipo funcional em Python (PyTorch) focado no ensino de programação Python. Diferente do artigo completo, a implementação atual simplifica o *Structural Encoder*, focando na GRU e embeddings estáticos, mas prepara o terreno para a GNN.

### Domínio de Dados (Python Programming)
O sistema opera com 5 conceitos hierárquicos e 15 questões reais:
1.  **Variáveis e Tipos** (Nível 1)
2.  **Operadores** (Nível 1) -> Depende de Variáveis
3.  **Condicionais** (Nível 2) -> Depende de 1 e 2
4.  **Loops** (Nível 2) -> Depende de 1 e 2
5.  **Funções** (Nível 3) -> Depende de 3 e 4


### Modelo Atual (PyTorch)
* **Entrada:** `Embedding(Conceito) + Resultado_Anterior (0 ou 1)`.
* **Core:** `GRU (Hidden Size=16, Layers=1)`.
* **Saída:** Probabilidade (Sigmoid) de acerto na próxima questão.
* **Status:** O modelo aprende padrões sequenciais e proficiência latente, mas ainda não utiliza GNNs (Graph Neural Networks) para processar o grafo explicitamente durante o forward pass.

---

## 4. Arquitetura Alvo: Microserviço Jedai_SINKT

O objetivo imediato é transformar o notebook em uma API que se comunica com o ecossistema "Jedai" (Plataforma de Ensino) e "MAIC" (Agentes Pedagógicos).

### Fluxo de Dados da API
1.  **Input (Request):** O aluno responde uma questão no frontend.
    * Payload: `{ "user_id": "Aluno_1", "question_id": "Q010", "concept_id": "loops", "result": 1 }`
2.  **Processamento SINKT:**
    * Carrega o histórico do aluno (banco de dados ou memória).
    * Gera o vetor de estado oculto atualizado via GRU.
    * Calcula a probabilidade de domínio atual ($p$) para o conceito trabalhado e próximos conceitos.
3.  **Lógica de Negócio (Pedagogia):**
    * Se $p < 0.4$: Acionar intervenção (MAIC).
    * Se $0.4 \le p \le 0.8$: Continuar prática no mesmo conceito.
    * Se $p > 0.8$: Sugerir avanço para próximo nó do grafo.
4.  **Output (Response):**
    * JSON contendo: Probabilidade de domínio, Próxima Ação Sugerida, Validação de Pré-requisitos.

---

## 5. Prompts e Uso de LLM (Integração)

O arquivo `prompts.json` define como as LLMs auxiliam o SINKT na fase de **Indução** (adicionar novos conteúdos sem re-treinar a rede neural do zero).

1.  **`concept_to_related_concepts`:** Define a topologia do grafo (pré-requisitos) quando um novo conceito é criado.
2.  **`question_to_concepts`:** Classifica uma nova questão automaticamente para vinculá-la a um nó do grafo.
3.  **`generate_question_for_concepts`:** (MAIC) Gera questões sintéticas para preencher lacunas de dados no grafo.

**Regra de Ouro:** O SINKT usa LLMs para *estruturar os dados* (grafo e texto), mas usa a Rede Neural (GRU/GNN) para *prever o desempenho* (velocidade e precisão).

---

## 6. Diretrizes para Implementação da API

Ao gerar código ou sugerir arquitetura para este contexto, siga estas regras:

1.  **Modularidade:** Separe a lógica do modelo (`model.py`), o carregamento de dados (`data_loader.py`) e as rotas da API (`main.py` / `routes.py`).
2.  **Persistência:** O estado oculto ($h_t$) da GRU precisa ser persistido por aluno. Inicialmente, pode ser em memória ou arquivo, mas planeje para Redis/Postgres.
3.  **Embeddings:** Os embeddings treinados no notebook devem ser salvos (`state_dict`) e carregados na inicialização da API. Não treine o modelo a cada request.
4.  **Grafo:** O grafo (NetworkX) deve ser carregado na memória para verificar pré-requisitos rapidamente (ex: "Aluno pode acessar Funções?").
5.  **Type Hinting:** Use Pydantic para validação de dados de entrada/saída da API.

## 7. Terminologia Chave
* **KC (Knowledge Component):** Sinônimo de Conceito ou Habilidade.
* **KT (Knowledge Tracing):** A tarefa de modelar o conhecimento do aluno ao longo do tempo.
* **Inductive:** Capacidade de lidar com itens não vistos no treino.
* **Transductive:** Limitação de lidar apenas com itens fixos (IDs conhecidos).
* **Cold Start:** Problema de não ter dados históricos sobre um novo aluno ou nova questão.