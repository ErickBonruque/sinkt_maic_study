# SINKT Base Individual - Projeto Completo (Dataset Realista)

#### Conceitos Reais de Python:
1. **Variáveis e Tipos de Dados** - int, float, str, bool
2. **Operadores Aritméticos e Lógicos** - +, -, *, /, ==, !=, and, or, not
3. **Estruturas Condicionais** - if/elif/else
4. **Estruturas de Repetição** - for/while, range(), break, continue
5. **Funções** - def, parâmetros, return, escopo

#### Questões Verdadeiras:
- **15 questões reais** com enunciados completos
- **3 questões por conceito**
- **Exemplos:**
  - Q001: "Qual é o tipo de dado da variável `x = 10`?"
  - Q010: "Quantas vezes executa: `for i in range(5): print(i)`?"
  - Q013: "Qual a saída de: `def soma(a,b): return a+b; print(soma(3,5))`?"

---

## Como Usar

```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Instalar dependências
pip install torch networkx matplotlib pandas numpy scikit-learn jupyter

# 3. Iniciar Jupyter
jupyter notebook SINKT_Base_Individual_v2.ipynb
```

---

## O que o Notebook Contém

### 1. Conceitos e Questões Reais (Seção 2)
- **Carregamento de dados dos CSVs** (`data/conceitos.csv`, `data/questoes.csv`, `data/grafo_prerequisitos.csv`)
- **5 conceitos** de programação Python
- **15 questões** verdadeiras com enunciados completos
- **Dificuldades:** fácil, médio
- **Mapeamento** questão → conceito

### 2. Dataset Realista (Seção 3)
- **10 alunos** (Aluno_1 a Aluno_10)
- **~50 tentativas** simuladas
- **Proficiência variável** por aluno (0.3 a 0.9)
- **Probabilidade de acerto** baseada em proficiência × dificuldade
- Colunas: `aluno`, `questao_id`, `questao_texto`, `conceito_id`, `conceito_nome`, `dificuldade`, `acerto`

### 3. Integração com Gemini AI (Fase Indutiva - Seção 4)
- **Modelo:** `gemini-2.0-flash` via `google-generativeai`.
- **Geração de Grafo:** O grafo de pré-requisitos é construído dinamicamente pela IA.
  - Prompt: `concept_to_related_concepts`.
  - Identifica dependências lógicas entre os conceitos (ex: Loops dependem de Condicionais).
- **Classificação de Questões:** Teste de capacidade da IA de mapear novas questões para os conceitos existentes.
  - Prompt: `question_to_concepts`.
  - Exemplo validado com questão inédita envolvendo loops e condicionais.

### 4. Embeddings (Seção 5)
- Vetores de **8 dimensões** para cada conceito
- Entrada da GRU = embedding do conceito + flag de acerto anterior

### 5. Implementação da GRU (Seção 7)
- `hidden_size = 16`
- `num_layers = 1`
- `epochs = 5` (mais epochs para melhor aprendizado)
- Loss: Binary Cross Entropy (BCEWithLogitsLoss)
- Otimizador: Adam

### 6. Predições (Seção 9)
- Seleciona aluno específico (Aluno_1)
- Alimenta sequência de tentativas na GRU
- Prevê probabilidade de acerto para cada questão
- Exibe resultados com questões reais e conceitos

### 7. Mini-Relatório Individual (Seção 11)
- O que entendi sobre o funcionamento da GRU **com dados reais**
- Como ela aprende com a sequência de acertos/erros **em questões de Python**
- O que ainda ficou com dúvida
- Qual parte foi mais fácil / mais difícil
- Como o grafo conceitual influenciou as predições
- **Integração detalhada com Jedai-SINKT** (arquitetura + exemplos práticos)

---

## Visualizações Geradas

O notebook gera automaticamente as seguintes visualizações na pasta `outputs/`:

1. **`outputs/grafo_conceitual_python.png`** - Estrutura de pré-requisitos com nomes completos
2. **`outputs/loss_curve_realista.png`** - Curva de aprendizado (train vs test loss)
3. **`outputs/predicoes_analise_realista.png`** - Análise de predições vs realidade com conceitos reais
4. **`outputs/embeddings_similaridade_python.png`** - Matriz de similaridade entre conceitos de Python