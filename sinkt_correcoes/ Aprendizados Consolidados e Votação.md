# Aprendizados Consolidados e Votação – FASE 3 SINKT

Este documento consolida os aprendizados obtidos a partir da revisão técnica cruzada dos notebooks da FASE 2, conforme o objetivo de aprofundar o entendimento sobre o pipeline SINKT.

---

## 1. O que aprendi analisando o código dos outros

A análise comparativa dos diferentes notebooks foi extremamente valiosa e revelou uma diversidade de abordagens para resolver o mesmo problema, cada uma com seus pontos fortes. Os principais aprendizados foram:

- **A Importância da Semântica nos Embeddings (TIEnc):** Meu notebook inicial utilizava embeddings aleatórios, que não carregam nenhum significado. Ao analisar o trabalho de **Lucas Parteka**, ficou evidente que o uso de um modelo de linguagem pré-treinado como o **BERT** para gerar os embeddings textuais (TIEnc) é um salto de qualidade fundamental. Essa abordagem, alinhada ao paper do SINKT, cria representações vetoriais ricas em semântica para conceitos e questões, o que potencializa a capacidade do modelo de generalizar e entender as relações de conteúdo.

- **O Poder da Estrutura do Grafo (SIEnc):** Apenas criar um grafo de pré-requisitos não é suficiente; é preciso processá-lo para que o modelo extraia valor dessa estrutura. As implementações de **Caio Wanderly** e **Lucas Parteka** com **GAT (Graph Attention Network)** para o SIEnc foram um grande insight. A GAT permite que o modelo aprenda dinamicamente a importância de cada relação no grafo (conceito-conceito, conceito-questão), refinando os embeddings de uma maneira que uma simples agregação não conseguiria.

- **Modularidade e Boas Práticas de Código:** Os notebooks de **Matheus Lacerda** e **Caio Wanderly** se destacaram pela excelente organização e modularidade, encapsulando cada componente do pipeline (Dataset, TIEnc, SIEnc, GRU) em classes distintas. Isso não apenas torna o código mais legível e profissional, mas também facilita a manutenção, o reuso e a depuração. Adotar essa estrutura é uma melhoria clara para o meu próprio código.

- **Simulação Realista de Dados:** A criação do dataset é uma etapa crítica. **Héber Júnior** e **Eduardo Prasniewski** mostraram abordagens sofisticadas para simular o comportamento dos alunos, introduzindo conceitos como habilidade inata, dificuldade progressiva e fatores de aprendizado/esquecimento. Isso gera um histórico de interações mais próximo da realidade, resultando em um treinamento de modelo mais robusto.

---

## 2. O que ficou mais claro sobre o pipeline

A revisão cruzada solidificou meu entendimento do pipeline completo, especialmente sobre como os componentes se conectam e a importância de cada um:

- **Dataset → Grafo:** O dataset não serve apenas para o treinamento da GRU, mas é a fonte primária para a construção do grafo heterogêneo, que conecta alunos, questões e conceitos.
- **Grafo → Embeddings (SIEnc):** O propósito do SIEnc ficou muito mais claro: ele não substitui os embeddings textuais (TIEnc), mas os **enriquece**. O processo é: 1) Gerar embeddings semânticos com BERT (TIEnc); 2) Usar a GAT (SIEnc) para agregar informações estruturais dos vizinhos no grafo a esses embeddings, criando uma representação final que une semântica e estrutura.
- **Embeddings → GRU:** A GRU não recebe apenas um ID da questão, mas sim o **embedding enriquecido** da interação (que combina o embedding da questão e o resultado do acerto/erro). Isso permite que o estado oculto da GRU (que representa o conhecimento do aluno) seja atualizado com base em informações muito mais ricas.
- **GRU → Predição:** A predição para uma nova questão `q_t+1` é feita combinando o estado de conhecimento atual do aluno (saída da GRU) com o embedding da nova questão. A interação entre esses dois vetores determina a probabilidade de acerto.

O pipeline, portanto, é uma cascata onde cada etapa refina e agrega valor à informação que será utilizada pela etapa seguinte.

---

## 3. Erros, Riscos ou Inconsistências Encontrados

Durante a análise, identifiquei alguns riscos e pontos de atenção comuns:

- **Risco de Embeddings Simplistas:** Notebooks que utilizam embeddings aleatórios (como o meu, inicialmente) correm o risco de ter um modelo com baixo desempenho, pois falta a informação semântica necessária para que a GRU e a GAT operem de forma eficaz.
- **Subutilização do Grafo:** Alguns notebooks constroem o grafo, mas não o utilizam efetivamente para enriquecer os embeddings (ausência de uma GNN como GAT ou GCN). Nesses casos, o grafo serve apenas para visualização, o que é uma subutilização do seu potencial.
- **Complexidade da Geração do Dataset:** A lógica para gerar um dataset sintético pode se tornar muito complexa e, se não for bem documentada, pode ser difícil de entender e replicar. É crucial equilibrar realismo com simplicidade.
- **Falta de Validação Cruzada:** A maioria dos notebooks (incluindo o meu) utiliza uma simples divisão treino/teste. Para um resultado mais robusto e para avaliar a estabilidade do modelo, a implementação de validação cruzada (como K-Fold) seria uma melhoria importante, como sugerido no meu plano de ação.

---

## 4. Dúvidas que Surgiram

- Como o SINKT lida com o problema do "cold start" para **novos alunos** (e não apenas novas questões)? O paper foca na natureza indutiva para questões, mas a abordagem para alunos com zero histórico de interações ainda não está totalmente clara para mim.
- Qual o impacto real do **Jumping Knowledge (JK)** no SIEnc? Nenhum dos notebooks implementou essa técnica, e seria interessante investigar se ela traz um ganho significativo de performance ao preservar o embedding textual inicial.
- Em um cenário de produção, com que frequência o **grafo de pré-requisitos** deveria ser atualizado pela LLM? Seria um processo em batch periódico ou uma atualização em tempo real a cada novo conceito adicionado?

---

## 6. Eleição do Melhor Código da FASE 2

**Meu voto:** Matheus Lacerda

**Justificativa:**

O notebook de Matheus Lacerda foi, em minha avaliação, o mais completo e bem executado. Ele implementou todos os 7 componentes do pipeline de forma clara e funcional, com destaque para a **integração com a LLM para geração dinâmica do grafo**, que era um dos pontos mais desafiadores. O código é altamente modular, com uso consistente de classes e funções, e a presença de tratamento de erros e logging demonstra uma maturidade técnica e uma preocupação com a robustez que o diferencia dos demais. Embora não tenha implementado GAT ou BERT, sua estrutura de código é a mais sólida e preparada para receber essas melhorias, servindo como a melhor base para a construção do nosso "Jedai_SINKT".
