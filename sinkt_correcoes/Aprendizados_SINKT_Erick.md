# Aprendizados da Análise Cruzada do SINKT - Fase 2

## 1. O que aprendi analisando o código dos outros

A revisão dos notebooks dos colegas de equipe revelou diversas abordagens e técnicas para a implementação do pipeline SINKT. A seguir, apresento os principais aprendizados obtidos a partir da comparação entre as diferentes soluções.

### Boas Práticas e Inovações Observadas

- **Modularização e Clareza:** Notebooks como os de **Matheus Lacerda** e **Lucas Timoteo** se destacaram pela excelente organização do código em classes e funções, com *type hints* e *docstrings*. Essa abordagem, embora mais verbosa, torna o pipeline muito mais legível, manutenível e fácil de depurar. O notebook do Caio também apresentou uma boa estrutura modular.

- **Implementações Avançadas de SIEnc:** O notebook de **Lucas Parteka** foi notável por ser um dos únicos a implementar o **GAT (Graph Attention Network)** para o *Structural Information Encoder (SIEnc)*, uma abordagem mais sofisticada e alinhada ao paper original do SINKT. Além disso, ele também explorou o uso do **BERT** para o *Textual Information Encoder (TIEnc)*, o que representa um avanço significativo em relação à simples criação de embeddings aleatórios.

- **Integração com LLMs:** Assim como no meu notebook, os trabalhos de **Matheus Lacerda** e **Lucas Timoteo** também integraram com sucesso um LLM (Gemini/OpenAI) para a geração dinâmica do grafo de pré-requisitos entre conceitos. Isso demonstra um entendimento claro da fase indutiva do SINKT, onde o modelo deve ser capaz de se adaptar a novos conceitos.

- **Documentação e Visualização:** A maioria dos notebooks apresentou um bom trabalho na documentação com Markdown e na geração de visualizações (grafos, curvas de perda, etc.), o que é fundamental para a interpretabilidade do modelo. O trabalho de **Héber Júnior** se destacou pela documentação detalhada e clara.

### Pontos de Melhoria Comuns

- **Complexidade do Pipeline:** Em alguns casos, a implementação do pipeline estava incompleta, faltando componentes essenciais como a camada de embeddings, claro que eram apenas testes e não implementações completas. Isso reforça a importância de garantir que todas as etapas (Dataset → Grafo → Embeddings → GRU → Predição) estejam presentes e conectadas.

- **Falta de Documentação:** Alguns documentos embora tecnicamente sólidos, senti a falta de células de Markdown explicativas, dificultando o entendimento do raciocínio por trás do código.

## 2. O que ficou mais claro sobre o pipeline SINKT

Analisar as diferentes implementações consolidou meu entendimento sobre a arquitetura do SINKT e a função de cada componente:

- **TIEnc e SIEnc:** Ficou evidente a importância dos dois encoders. O **TIEnc (com BERT)** captura a semântica dos textos de conceitos e questões, enquanto o **SIEnc (com GAT ou similar)** enriquece esses embeddings com a informação estrutural do grafo de pré-requisitos. A combinação de ambos é o que torna o SINKT poderoso.

- **A Natureza Indutiva:** A capacidade de adicionar novos nós (conceitos/questões) ao grafo e gerar seus embeddings sem a necessidade de retreinar todo o modelo a partir do zero é o principal diferencial do SINKT. A integração com LLMs para gerar as arestas de pré-requisitos é uma forma prática de realizar essa etapa.

- **O Papel da GRU:** A GRU funciona como a memória do modelo, rastreando o estado de conhecimento do aluno ao longo do tempo. A forma como a entrada da GRU é construída (concatenando o embedding do conceito com um indicador de acerto/erro) é um detalhe crucial que eu não havia compreendido totalmente antes.

## 3. Erros, Riscos ou Inconsistências Encontrados

- **Ausência de Validação Cruzada:** A maioria dos trabalhos, incluindo o meu, se limitou a uma simples divisão treino/teste. Para um modelo mais robusto, a implementação de uma validação cruzada (k-fold) seria ideal para garantir que o desempenho não é apenas um artefato da divisão de dados escolhida.

- **Inconsistência na Simulação de Dados:** As lógicas para gerar os datasets sintéticos variaram bastante, algumas mais realistas que outras. Isso pode levar a conclusões diferentes sobre a eficácia do modelo, destacando a necessidade de um dataset padronizado para comparação justa.

## 4. Dúvidas que Surgiram

- Qual o impacto real da qualidade do grafo de pré-requisitos no desempenho final? Um grafo gerado por LLM é significativamente melhor que um grafo mais simples?
- Como o SINKT se comportaria com um número muito maior de conceitos e questões? A complexidade do GAT/GRU escalaria bem?
- Qual a melhor estratégia para o TIEnc? BERT, ou um modelo mais simples como Word2Vec/GloVe seria suficiente para capturar a semântica necessária?

