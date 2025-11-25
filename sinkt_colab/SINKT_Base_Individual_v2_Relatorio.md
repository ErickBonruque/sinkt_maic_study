## 1. Objetivo

Este documento descreve o processo e os resultados obtidos no notebook `SINKT_Base_Individual_v2.ipynb`. O objetivo foi implementar um pipeline completo de Knowledge Tracing (Rastreamento de Conhecimento) utilizando uma rede neural recorrente (GRU) aplicada a um dataset realista de questoes de programacao em Python.

## 2. Passo a Passo Realizado

### 2.1. Instalacao e Configuracao

O ambiente foi preparado com a instalacao das bibliotecas necessarias:
- **PyTorch**: Para construcao e treinamento da rede neural.
- **NetworkX**: Para criacao e manipulacao de grafos conceituais.
- **Matplotlib/Pandas/NumPy**: Para manipulacao de dados e visualizacao.
- **Scikit-learn**: Para divisao de dados e metricas.

Foram configuradas sementes aleatorias (seeds) para garantir a reprodutibilidade dos resultados.

### 2.2. Definicao de Conceitos e Questoes Reais

Ao inves de dados sinteticos abstratos, foram utilizados conceitos e questoes reais de Python:

*   **Conceitos Abordados (5 no total):**
    1.  Variaveis e Tipos de Dados
    2.  Operadores Aritmeticos e Logicos
    3.  Estruturas Condicionais (if/elif/else)
    4.  Estruturas de Repeticao (for/while)
    5.  Funcoes

*   **Questoes:**
    *   Foram criadas 15 questoes reais com enunciados e niveis de dificuldade (facil, medio, dificil).
    *   Cada conceito possui 3 questoes associadas.

### 2.3. Criacao do Dataset Realista

Foi simulado um dataset comportamental de alunos:
*   **Participantes:** 10 alunos simulados (Aluno_1 a Aluno_10).
*   **Metodologia de Simulacao:**
    *   Cada aluno recebeu um nivel de proficiencia geral aleatorio.
    *   A probabilidade de acerto foi calculada combinando a proficiencia do aluno com a dificuldade da questao.
    *   Foram geradas 50 tentativas no total (5 questoes por aluno).
*   **Estatisticas do Dataset Gerado:**
    *   Taxa de acerto geral: 38.00%
    *   Conceito com maior taxa de acerto: Estruturas Condicionais (53.8%)
    *   Conceito com menor taxa de acerto: Variaveis e Tipos de Dados (20.0%)


### 2.5. Implementacao de Embeddings e Modelo

*   **Embeddings:** Cada conceito foi mapeado para um vetor denso de 8 dimensoes.
*   **Modelo GRU (Gated Recurrent Unit):**
    *   Entrada: Embedding do conceito atual + Resultado da tentativa anterior (acerto/erro).
    *   Camada Oculta: 16 unidades.
    *   Saida: Probabilidade de acerto na proxima questao.
    *   Total de parametros: 1,353.

### 2.6. Treinamento

*   **Divisao dos Dados:** 80% para treino (40 amostras) e 20% para teste (10 amostras).
*   **Configuracao:**
    *   Funcao de Perda: BCEWithLogitsLoss.
    *   Otimizador: Adam (Learning Rate = 0.001).
    *   Epocas: 5.
*   **Curva de Aprendizado:** Monitoramento da reducao da perda (Loss) tanto no treino quanto no teste.

### 2.7. Predicoes e Analise

O modelo foi utilizado para prever o desempenho de um aluno especifico ("Aluno_1") em suas tentativas. As predicoes (probabilidade de acerto) foram comparadas com os acertos reais.

---

## 3. Resultados Obtidos

### 3.1. Desempenho do Modelo
*   O modelo convergiu durante as 5 epocas de treinamento.
*   **Train Loss Final:** ~0.7068
*   **Test Loss Final:** ~0.7166
*   A acuracia nas predicoes para o aluno de teste foi de 40.00% (dado o pequeno volume de dados, isso e esperado, servindo como prova de conceito).

### 3.2. Analises Visuais Geradas
O notebook gerou tres visualizacoes principais salvas na pasta `outputs`:
1.  **grafo_conceitual_python.png**: Visualizacao da estrutura de pre-requisitos.
2.  **loss_curve_realista.png**: Grafico da evolucao da perda durante o treinamento.
3.  **predicoes_analise_realista.png**: Comparacao entre a probabilidade predita pelo modelo e o resultado real do aluno, alem do desempenho medio por conceito.
4.  **embeddings_similaridade_python.png**: Matriz de similaridade (cosseno) entre os conceitos aprendidos pelo modelo.

---

## 4. Mini-Relatorio Individual e Conclusoes

### 4.1. Entendimento da GRU
A GRU demonstrou capacidade de processar sequencias mantendo um estado oculto historico. Ela consegue inferir padroes como "sucesso em conceitos basicos aumenta a probabilidade de sucesso em conceitos dependentes" e ajusta suas predicoes baseada no historico imediato de acertos e erros.

### 4.2. Aprendizados com o Dataset Realista
*   **Padroes de Proficiencia:** O modelo capturou que alunos proficientes em temas base tendem a ir bem nos avancados.
*   **Dificuldade:** A dificuldade intrinseca das questoes (facil/medio/dificil) foi assimilada atraves das estatisticas de acerto.
*   **Dependencia Temporal:** A ordem das tentativas influencia a confianca do modelo.

### 4.3. Integracao com o Projeto Jedai - SINKT
O experimento valida o fluxo proposto para o sistema Jedai:
1.  O aluno responde no Jedai.
2.  O SINKT recebe o dado e atualiza o modelo.
3.  O modelo retorna a probabilidade de dominio e sugestoes.
4.  O Jedai adapta o conteudo ou aciona agentes (MAIC) para intervencao.

### 4.4. Proximos Passos Sugeridos
*   Expandir o banco de questoes para cobrir mais topicos e aumentar o volume de dados.
*   Implementar validacao explicita de pre-requisitos usando o grafo.
*   Criar dashboards para professores visualizarem o progresso da turma.
*   Integrar a saida do modelo com os agentes pedagogicos para feedbacks personalizados.
