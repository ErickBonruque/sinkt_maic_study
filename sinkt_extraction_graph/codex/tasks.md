# Projeto: Extração e Validação de Conceitos para SINKT

## 🎯 Objetivo Geral
Garantir que a extração de conceitos do **SINKT** produza resultados corretos, completos e coerentes. O objetivo é validar diferentes técnicas e estratégias de Engenharia de Dados e IA para criar um grafo de conhecimento educacional robusto.

### Foco
Validar e comparar diferentes estratégias de extração de conceitos, garantindo **qualidade máxima** antes da etapa de geração de grafos e rastreamento de conhecimento.

---

## 🔧 Metodologia e Atividades

A execução do projeto é dividida em 6 etapas principais:

### 1. Extração Inicial
* Realizar a extração a partir do material (PDF) utilizando técnica inicial.
* Identificar relações mínimas obrigatórias: `definition`, `prerequisite`, `property`, `part-of`, `including`.

### 2. Validação Cruzada (Cross-LLM)
* **Modelos de Teste:** OpenAI (GPT-3.5/4.x/5.x ou equivalentes atuais) e Claude (Opus/Sonnet).
* **Estratégia:** Uma LLM gera, outra valida. Inversão de papéis para evitar viés.

### 3. Validação Multi-Agentes (Debate)
* **Qtd. Mínima:** 8 Agentes Independentes.
* **Personas:**
    * *Proponentes:* Sugerem conceitos.
    * *Críticos:* Apontam falhas e redundâncias.
    * *Moderador:* Organiza o fluxo.
    * *Consenso:* Define a versão final.
    * *Auditor:* Garante o cumprimento das regras.

### 4. Consolidação
* Integrar resultados, remover inconsistências e padronizar nomenclaturas (tipagem canônica).

### 5. Validação Estrutural do Grafo
* Verificar integridade topológica (nós órfãos, ciclos em pré-requisitos, hierarquia lógica).

### 6. Entregáveis Obrigatórios
* **Relatório Técnico:** Metodologia, evidências, logs de debate e conclusão sobre a melhor técnica.
* **Notebook Colab:** Código reproduzível do pipeline completo.

---

## ✅ Checklist de Execução

Marque as tarefas conforme o progresso:

- [x] **Realizar a extração a partir do material utilizando qualquer técnica** (Feito: `1_concept_extraction.ipynb`)
- [x] **Identificar relações mínimas** (definition, prerequisite, property, part-of, including) (Feito: `2_relation_extraction.ipynb`)
- [x] **Validação Cruzada entre Múltiplas LLMs** (Adaptado: Validação via Agente Architect no `3_multi_agent_densification.ipynb`)
- [x] **Validação com agentes** (Debate estruturado simplificado com 3 personas: Cleaner, Architect, Teacher)
- [x] **Integrar resultados validados pelas LLMs e agentes** (Implementado no `4_final_validation_pipeline.ipynb`)
- [x] **Remover redundâncias e inconsistências** (Iniciado com Agente Cleaner, finalizar na Consolidação)
- [x] **Ajustar nomenclaturas** (Canonicalização de Tipos via Agente Terminologista no NB 4)
- [x] **Preparar conjunto final para montagem do grafo** (Implementado no `4_final_validation_pipeline.ipynb`)
- [x] **Verificar nós órfãos** (Densificação e Limpeza no NB 4)
- [x] **Verificar ciclos indevidos** (Remoção de Ciclos no NB 4)
- [x] **Verificar coerência hierárquica** (Agente Topólogo no NB 4)
- [ ] **Garantir que todas as relações tenham justificativa e suporte textual**
- [ ] **Confirmar que o grafo representa fielmente o conteúdo**
- [ ] **Relatório Técnico Detalhado**
- [x] **Notebook Colab Final** (Criado: `4_final_validation_pipeline.ipynb`)

---

## 🏆 Resultados Esperados
* Conjunto final de conceitos e relações limpo e estruturado.
* Estratégia de extração vencedora documentada.
* Alinhamento completo entre as frentes de LLM e Dados.
* Pipeline pronto para a etapa de Rastreamento de Conhecimento (Knowledge Tracing).