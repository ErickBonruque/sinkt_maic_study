# Notas sobre o Modelo MAIC

**Data:** 16 de novembro de 2025  
**Fonte:** Paper "From MOOC to MAIC: Reshaping Online Teaching and Learning through LLM-driven Agents"

## O que é MAIC?

MAIC (Massive AI-empowered Course) é uma nova forma de educação online que utiliza sistemas multi-agentes baseados em LLMs para criar uma sala de aula aumentada por IA, balanceando escalabilidade com adaptabilidade.

## Diferença Principal: MOOC vs MAIC

### MOOC (Massive Open Online Course)
- **Ensino:** 1 vídeo gravado para N alunos
- **Custo:** $25,000 e 60 horas para criar um curso
- **Abordagem:** Conteúdo pré-gravado, estático
- **Limitação:** Sem personalização individual

### MAIC
- **Ensino:** N agentes IA para 1 aluno
- **Custo:** Menos de $2 e 30 minutos por curso
- **Abordagem:** Conteúdo dinâmico gerado por IA
- **Vantagem:** Personalização completa e adaptativa

## Arquitetura do MAIC

### 1. Lado do Ensino (Teaching Side)

**Etapa 1: Read (Leitura)**
- Professor faz upload dos slides do curso
- LLM multimodal extrai:
  - Conteúdo textual (Pᵢᵗ)
  - Conteúdo visual (Pᵢᵛ)
  - Descrição da página (Dᵢ)
  - Estrutura de conhecimento (Kⱼ) - taxonomia em árvore

**Etapa 2: Plan (Planejamento)**
- Sistema gera funções de ensino (Teaching Actions):
  - **ShowFile:** Mostrar próximo slide
  - **ReadScript:** Ler script baseado no slide atual
  - **AskQuestion:** Fazer perguntas após cada seção
- Gera agentes de ensino:
  - **Teacher Agent:** Agente professor principal
  - **Teaching Assistant:** Assistente de ensino
  - **Manager Agent:** Controla o fluxo da aula

### 2. Lado do Aprendizado (Learning Side)

**Ambiente Multi-Agente de Sala de Aula:**

O MAIC cria uma sala de aula virtual com múltiplos agentes IA que interagem com o aluno, simulando diferentes papéis e personalidades.

#### Agentes de Sala de Aula (Classmate Agents)

Quatro tipos principais de agentes-alunos foram criados, cada um com personalidade e função específica:

1. **Class Clown (TI, EC, CM)**
   - Função: Criar ambiente descontraído e engajador
   - Comportamento: Faz comentários divertidos, mantém o clima leve
   - Objetivo pedagógico: Reduzir ansiedade, manter atenção

2. **Deep Thinker (TI, ID)**
   - Função: Fazer perguntas profundas e provocativas
   - Comportamento: Questiona conceitos, busca aprofundamento
   - Objetivo pedagógico: Estimular pensamento crítico

3. **Note Taker (TI, CM)**
   - Função: Resumir e organizar informações
   - Comportamento: Destaca pontos-chave, faz sínteses
   - Objetivo pedagógico: Auxiliar na retenção de informação

4. **Inquisitive Mind (TI, EC)**
   - Função: Fazer perguntas sobre o conteúdo
   - Comportamento: Busca esclarecimentos, promove diálogo
   - Objetivo pedagógico: Estimular engajamento ativo

**Legenda dos papéis:**
- **TI:** Teaching and Initiation (Ensino e Iniciação)
- **ID:** In-depth Discussion (Discussão Aprofundada)
- **EC:** Emotional Companionship (Companheirismo Emocional)
- **CM:** Classroom Management (Gerenciamento de Sala)

#### Session Controller (Controlador de Sessão)

Componente central que gerencia o fluxo da aula:

**Class State Receptor:**
- Captura o diálogo em andamento
- Histórico até o tempo t: Hₜ = ⋃(uᵢᵃʲ)ᵗ
- Estado da classe: Sₜ = {Pₜ, Hₜ|R̃}
- Pₜ: materiais de aprendizado cobertos até o momento

**Manager Agent:**
- Agente meta-gerenciador oculto
- Recebe o estado atual da classe Sₜ
- Monitora o fluxo da aula
- Determina a próxima ação a ser executada
- Função: fC: Sₜ → (aᵢ, T̃)|aᵢ ∈ A, T̃ₙ ⇐ T

**Princípios Pedagógicos Implementados:**

Baseado no trabalho de Schwanke (1981), o MAIC implementa três comportamentos principais:

1. **Teaching and Initiation (TI):**
   - Ações instrutivas do professor
   - Feedback responsivo aos alunos

2. **In-depth Discussion (ID):**
   - Alinhamento e deliberação
   - Troca iterativa de perguntas e respostas
   - Facilita compreensão conceitual

3. **Emotional Companionship (EC):**
   - Encorajamento do aprendizado
   - Cultivo de ambiente de aprendizado positivo
   - Suporte emocional

4. **Classroom Management (CM):**
   - Manutenção da ordem
   - Organização de elementos disruptivos
   - Direcionamento do discurso da sala

## Resultados do Experimento

### Experimento na Tsinghua University
- Mais de 100,000 registros de aprendizado
- Mais de 500 estudantes voluntários
- Dois cursos testados:
  - "Towards Artificial General Intelligence" (TAGI)
  - "How to Study in the University" (HSU)

### Avaliação de Qualidade

**Métricas de Script (escala Likert 1-5):**
- **Tone:** Tom apropriado de professor (4.00)
- **Clarity:** Clareza e compreensibilidade (4.25)
- **Supportive:** Suporte emocional e motivacional (3.57)
- **Matching:** Alinhamento com material dos slides (4.18)
- **Overall:** Desempenho geral (4.00)

**Comparação com humanos:**
- MAIC superou ligeiramente instrutores humanos em 3 dimensões
- LLMs aderem estritamente às instruções
- Humanos tendem a expandir tópicos livremente, divergindo do conteúdo

### Feedback dos Estudantes

**Aspectos Positivos (média > 3.7/5):**
- Objetivos do curso claros: 4.12
- Discussão de problemas: 3.91
- Exploração de novos conceitos: 4.03
- Envolvimento em tarefas: 3.85
- Clareza de pensamento: 3.85
- Compreensão de temas: 3.77

**Aspectos a Melhorar:**
- Feedback personalizado: 3.51
- Falta de adaptabilidade individual
- Scripts iguais para todos os alunos

## Cenários Típicos de Uso

### Modo Contínuo
- Aluno assiste sem interrupções
- Agentes IA conduzem a aula do início ao fim
- Abordagem mais passiva

### Modo Interativo
- Aluno pode interromper a qualquer momento
- Fazer perguntas ao professor IA
- Interagir com agentes-colegas
- Abordagem mais ativa

## Limitações Atuais

1. **Personalização limitada:** Mesmo script para todos os alunos
2. **Feedback genérico:** Não adapta totalmente ao desempenho individual
3. **Precisão do Manager Agent:** Ainda abaixo do ideal (60-80%)
4. **Dependência de LLMs:** Requer modelos de linguagem avançados

## Aplicações Práticas

1. **Criação rápida de cursos:** De 60h para 30min
2. **Redução de custos:** De $25k para <$2
3. **Escalabilidade:** Atender milhares de alunos simultaneamente
4. **Personalização:** Cada aluno tem seus próprios agentes IA
5. **Suporte emocional:** Agentes fornecem companheirismo
6. **Discussão ativa:** Ambiente de sala de aula simulado

## Comparação MAIC vs SINKT

### SINKT
- **Foco:** Rastreamento de conhecimento (Knowledge Tracing)
- **Objetivo:** Prever se o aluno acertará a próxima questão
- **Abordagem:** Modelagem matemática/estatística (BKT, grafos, LLMs)
- **Saída:** Probabilidade de domínio (p)
- **Uso:** Diagnóstico e predição

### MAIC
- **Foco:** Entrega de conteúdo e interação
- **Objetivo:** Ensinar e engajar o aluno
- **Abordagem:** Sistemas multi-agentes com LLMs
- **Saída:** Aulas interativas personalizadas
- **Uso:** Instrução e aprendizado ativo

### Complementaridade
- SINKT pode ser integrado ao MAIC para:
  - Adaptar o ritmo da aula baseado em p
  - Identificar conceitos que precisam de reforço
  - Personalizar intervenções dos agentes
  - Recomendar atividades baseadas no domínio atual
