# Explicação Técnica do Projeto SINKT

Este documento detalha o funcionamento interno do projeto SINKT (Structure-Aware Inductive Knowledge Tracing), focado em rastreamento de conhecimento para ensino de programação Python.

---

## 1. Análise de Loss e Accuracy

### O modelo está aprendendo de fato?
Sim, é possível verificar isso através das curvas de **Train Loss** (Erro de Treinamento) e **Test Loss** (Erro de Teste).

*   **Loss (Perda):** O gráfico no notebook mostra a Loss diminuindo ao longo das épocas (Epochs). Isso significa que a diferença matemática entre a previsão do modelo (ex: 0.7) e o valor real (ex: 1.0) está ficando cada vez menor.
*   **Accuracy (Acurácia):** Mede a porcentagem de vezes que o modelo acertou se o aluno erraria ou acertaria a questão (arredondando a probabilidade).

**Interpretação dos Resultados Atuais:**
No notebook analisado, a Loss cai de ~0.72 para ~0.70. Isso indica um aprendizado inicial. No entanto, como o dataset atual é pequeno (apenas 10 alunos simulados e 50 tentativas no total), o aprendizado é limitado e pode haver instabilidade.

### Com mais dados ele seria melhor?
**Definitivamente sim.** Redes Neurais como a GRU (Gated Recurrent Unit) são "famintas por dados".
*   **Poucos dados:** O modelo decora os exemplos (overfitting) ou não consegue encontrar padrões gerais.
*   **Mais dados:** Com milhares de alunos, o modelo conseguiria captar padrões sutis (ex: "alunos que erram 'loops' geralmente erram 'funções' logo em seguida"). Isso faria a Loss cair muito mais e a acurácia subir.

---

## 2. Cálculo de Acerto/Erro e Estado do Aluno ($p$)

### Como é o cálculo de acerto/erro na simulação?
No dataset sintético atual, o acerto não é apenas aleatório. Ele segue uma lógica probabilística para simular a realidade:

$$ P(\text{acerto}) = (\text{Proficiência do Aluno} \times \text{Dificuldade da Questão}) + \text{Ruído} $$

*   **Proficiência:** Um valor entre 0.3 e 0.9 atribuído a cada aluno.
*   **Dificuldade:** Um peso (Fácil=0.75, Médio=0.55, Difícil=0.35).
*   O código sorteia um número aleatório; se for menor que $P(\text{acerto})$, o aluno acerta (1), caso contrário, erra (0).

### Como é feita a atualização do estado de domínio ($p$)?
Diferente de modelos estatísticos clássicos (como BKT) que têm uma variável explícita $p$ para cada conceito, no SINKT com Deep Learning:

*   **O "estado do aluno" é o vetor oculto ($h$) da GRU.**
*   A cada nova questão respondida, a GRU atualiza esse vetor $h$ matemático.
*   Esse vetor contém, de forma comprimida e latente, todo o histórico do aluno. Ele não diz "o aluno sabe 80% de For", mas sim um vetor numérico que, quando processado, resulta na probabilidade de acerto futuro.

---

## 3. O que é a GRU e seu Cálculo

**GRU (Gated Recurrent Unit)** é um tipo de Rede Neural Recorrente otimizada para sequências temporais (como a ordem de aprendizado de um aluno).

### Como funciona (Simplificado):
Imagine que a GRU é uma "caixa de memória" que recebe duas coisas a cada passo:
1.  **Informação Nova:** A questão que o aluno acabou de responder e se ele acertou ou não.
2.  **Memória Anterior:** O estado da mente do aluno antes dessa questão.

Ela possui dois "portões" (gates) principais:
*   **Update Gate (Portão de Atualização):** Decide o quanto do passado deve ser mantido e o quanto da nova informação deve ser guardada.
*   **Reset Gate (Portão de Esquecimento):** Decide o que é irrelevante e deve ser esquecido (ex: um erro por distração que não reflete falta de conhecimento).

**No código (`SINKTModel`):**
```python
# Entrada: Embedding do Conceito + Acerto Anterior (0 ou 1)
x = torch.cat([emb, acerto_anterior], dim=1)

# Processamento pela GRU
# x: entrada atual
# hidden: estado mental anterior
gru_out, hidden = self.gru(x, hidden)
```

---

## 4. Como funcionam as Predições

O processo de predição segue este fluxo:

1.  **Input:** O modelo recebe o ID do conceito da próxima questão (ex: "Funções") e se o aluno acertou a questão *anterior*.
2.  **Embedding:** O ID do conceito é convertido em um vetor de números (embedding).
3.  **Processamento Recorrente:** A GRU pega esse vetor + o histórico acumulado do aluno (estado oculto) e gera um novo estado.
4.  **Camada Linear (Output):** O estado da GRU passa por uma camada linear (`self.fc`) que reduz tudo a um único número real.
5.  **Sigmoide:** Esse número passa pela função Sigmoide, que o espreme entre 0 e 1.
    *   Resultado `0.85`: O modelo prevê 85% de chance de acerto.
    *   Se `> 0.5`: Previsão final é **Acerto (1)**.
    *   Se `< 0.5`: Previsão final é **Erro (0)**.

---

## 5. Embeddings e Dependência de Conceitos (LLM)

### O Processo de Embedding
No código: `self.embedding = nn.Embedding(num_conceitos, 8)`
*   Cada conceito (ex: "Loop", "Variáveis") é transformado em um vetor de 8 números.
*   **O pulo do gato:** Inicialmente esses números são aleatórios. Durante o treinamento (backpropagation), o modelo **aprende** os melhores números para representar cada conceito. Conceitos similares (como "For" e "While") acabarão tendo vetores matematicamente próximos.

### Dependência de Conceitos (Fase Indutiva com LLM)
Aqui entra a inovação do SINKT para lidar com o "Cold Start" (quando não temos dados históricos suficientes para saber a ordem das matérias).

**Onde acontece:** Antes do treinamento da rede neural.
**Ferramenta:** Google Gemini 2.0 Flash.

#### Os Prompts Usados (`prompts.json`)

**1. Descobrir a Topologia (Pré-requisitos):**
*   **Prompt Key:** `concept_to_related_concepts`
*   **Objetivo:** Perguntar à IA: "Para aprender o conceito X, quais destes outros conceitos são pré-requisitos lógicos?"
*   **Uso no código:** Constrói o Grafo Direcionado (NetworkX) que desenha as setas entre as matérias.

**2. Classificar Questões (Labeling):**
*   **Prompt Key:** `question_to_concepts`
*   **Objetivo:** Dado o texto de uma questão, a IA diz a qual conceito ela pertence.
*   **Uso:** Permite pegar questões novas de um banco de dados desconhecido e inseri-las no sistema automaticamente.

**Resumo:** A LLM estrutura o conhecimento (cria o mapa do curso) e a GRU navega por esse mapa rastreando o aluno.
