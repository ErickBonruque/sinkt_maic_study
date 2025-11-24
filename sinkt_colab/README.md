# SINKT Base Individual - Projeto Completo (Dataset Realista)

**Autor:** Erick (Time de Dados - 4Linux)  
**Data:** Novembro de 2025  
**Versão:** 2.0 - Com conceitos e questões reais de Python

---

## Objetivo

Garantir que cada integrante dos times 4Linux, CEIA–LLM e CEIA–Dados consiga reproduzir individualmente um pipeline funcional do SINKT com **dados realistas**, passando por todas as etapas desde a construção do dataset até a interpretação dos resultados.

## Resultados Esperados

Ao final deste projeto, você será capaz de:

✅ Criar e executar seu próprio experimento do SINKT no Google Colab com **dados reais**  
✅ Explicar como a GRU aprende com sequências de acertos/erros em **questões verdadeiras de Python**  
✅ Demonstrar predições reais e gráficos interpretáveis  
✅ Entender o fluxo completo: curso → grafo → embeddings → GRU → domínio do aluno → predição  
✅ Relacionar o experimento ao futuro microserviço Jedai_SINKT

---

## Novidades da Versão 2.0

### Dataset Realista

Ao contrário da versão anterior (com conceitos K1-K5 e questões Q1-Q10), esta versão usa:

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

#### Grafo de Pré-requisitos Bem Definido:
```
variaveis_tipos → operadores
variaveis_tipos → condicionais
operadores → condicionais
variaveis_tipos → loops
operadores → loops
condicionais → funcoes
loops → funcoes
```

---

## Estrutura do Projeto

```
sinkt_colab/
│
├── README.md                          # Este arquivo
├── SINKT_Base_Individual_v2.ipynb     # Notebook principal (Google Colab)
│
├── data/                              # Dados de entrada (CSVs)
│   ├── conceitos.csv                  # Conceitos de Python
│   ├── questoes.csv                   # Questões reais
│   └── grafo_prerequisitos.csv        # Relações de pré-requisitos
│
└── outputs/                           # Saídas do notebook (gráficos)
    ├── grafo_conceitual_python.png
    ├── loss_curve_realista.png
    ├── predicoes_analise_realista.png
    └── embeddings_similaridade_python.png
```

---

## Como Usar

### Opção 1: Google Colab (Recomendado)

1. **Abrir no Google Colab:**
   - Faça upload do arquivo `SINKT_Base_Individual_v2.ipynb` no Google Drive
   - Abra com Google Colab
   - Ou acesse diretamente: [Link do Colab](#) (se disponível)

2. **Executar células sequencialmente:**
   - Clique em "Runtime" → "Run all" para executar tudo de uma vez
   - Ou execute célula por célula para acompanhar cada etapa

3. **Tempo estimado:**
   - Execução completa: ~5-10 minutos
   - Treinamento da GRU: ~2-3 minutos (5 epochs)

### Opção 2: Ambiente Local

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

### 3. Grafo Conceitual (Seção 4)
- **5 nós** (conceitos de Python)
- **7 arestas** de pré-requisito
- Visualização com nomes completos dos conceitos
- Exporta imagem como `grafo_conceitual_python.png`

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

---

## Integração com Jedai-SINKT

### Exemplo de Fluxo Completo

```
1. Aluno responde questão no Jedai:
   - Questão: Q010 ("Quantas vezes executa: for i in range(5)?")
   - Conceito: "Estruturas de Repetição (for/while)"
   - Resultado: Acerto (1)

2. Jedai envia para Jedai_SINKT:
   POST /sinkt/update
   {
     "user_id": "Aluno_1",
     "question_id": "Q010",
     "concept_id": "loops",
     "result": 1
   }

3. Backend Jedai_SINKT:
   - Recupera histórico: [variaveis_tipos:1, operadores:1, condicionais:0, loops:1]
   - Prepara entrada GRU: embeddings + sequência
   - Executa predição: p_dominio_loops = 0.68

4. Retorna para Jedai:
   {
     "p_dominio": 0.68,
     "conceito": "loops",
     "conceito_nome": "Estruturas de Repetição (for/while)",
     "proxima_acao": "continuar_pratica",
     "sugestao_questao": "Q011",
     "prerequisitos_ok": true,
     "pode_avancar_para": ["funcoes"]
   }

5. Jedai decide:
   - Como p = 0.68 (entre 0.4 e 0.8), continua praticando "Loops"
   - Apresenta Q011 ("O que imprime: for i in range(2, 6)?")
   - Se p subir para > 0.8, sugere avançar para "Funções"
   - Se p cair para < 0.4, aciona MAIC para intervenção
```

### Componentes do Microserviço

1. **Modelo GRU treinado** (arquivo .pth)
2. **Banco de conceitos e questões** (conceitos_questoes.py)
3. **Grafo conceitual** (estrutura de pré-requisitos)
4. **Embeddings dos conceitos**
5. **API REST** (Flask/FastAPI)
6. **Banco de dados** (histórico de tentativas)

### Endpoints Propostos

- `POST /sinkt/update` - Atualiza histórico e retorna predição
- `GET /sinkt/dominio/{user_id}` - Retorna p_dominio de todos os conceitos
- `GET /sinkt/pode_acessar/{user_id}/{concept_id}` - Valida pré-requisitos
- `GET /sinkt/explain/{user_id}/{concept_id}` - Explica a predição
- `GET /sinkt/grafo` - Retorna estrutura do grafo conceitual
- `GET /sinkt/questoes/{concept_id}` - Lista questões de um conceito

---

## Ideias para Melhorias Futuras

### 1. Banco de Questões Expandido
- Adicionar 100+ questões de Python
- Incluir mais conceitos (Listas, Dicionários, Classes, Exceções)
- Categorizar por dificuldade (fácil, médio, difícil, expert)

### 2. Validação de Pré-requisitos
- Bloquear acesso a "Funções" se p("Loops") < 0.6
- Sugerir revisão de pré-requisitos antes de avançar

### 3. Sugestão Inteligente de Questões
- Se p = 0.3 (baixo), sugerir questões fáceis
- Se p = 0.7 (médio), sugerir questões médias
- Se p = 0.9 (alto), sugerir questões difíceis ou avançar

### 4. Dashboard para Professores
- Visualizar p_dominio de todos os alunos em tempo real
- Identificar conceitos com baixo domínio geral
- Alertar sobre alunos em dificuldade

### 5. Integração com MAIC
- Se p < 0.4 em "Loops", ativar agentes pedagógicos
- Agente Tutor: perguntas socráticas
- Agente Conselho: estratégias de estudo
- Agente Amigo: suporte emocional

### 6. Explicabilidade
- Mostrar quais tentativas anteriores influenciaram a predição
- Sugerir conceitos pré-requisitos para revisão
- Visualizar trajetória de aprendizado

---

## Perguntas Frequentes

### P: Qual a diferença da versão 1.0 para a 2.0?

**R:** A versão 2.0 usa **conceitos e questões reais de Python** em vez de dados numéricos abstratos (K1-K5, Q1-Q10). Isso torna o modelo mais interpretável e próximo de um cenário real de ensino.

### P: Posso adicionar mais conceitos e questões?

**R:** Sim! Edite o arquivo `conceitos_questoes.py` para adicionar novos conceitos (ex: Listas, Dicionários) e questões. Lembre-se de atualizar o grafo de pré-requisitos.

### P: Como o modelo sabe que "Funções" depende de "Loops"?

**R:** Nesta implementação, o grafo é usado apenas para visualização e validação. A GRU aprende relações implícitas através dos dados. Em versões futuras, uma GNN pode usar o grafo explicitamente.

### P: Minha acurácia está baixa (<50%). É normal?

**R:** Com apenas 5 epochs e poucos dados, é normal. Tente aumentar `NUM_EPOCHS` para 10-20 e verificar se o loss está diminuindo.

### P: Como interpretar a matriz de similaridade dos embeddings?

**R:** Valores próximos de 1 indicam que dois conceitos são "similares" na visão do modelo. Isso pode significar que são frequentemente acertados/errados juntos, ou que têm pré-requisitos comuns.

---

## Checklist de Validação

Ao final da execução, você deve ser capaz de responder:

- [ ] O que é o estado oculto da GRU e como ele funciona?
- [ ] Como a GRU usa o acerto anterior para fazer predições?
- [ ] Por que embeddings são importantes?
- [ ] Como o grafo conceitual representa a estrutura de conhecimento de Python?
- [ ] Qual a diferença entre loss de treino e teste?
- [ ] Como interpretar a probabilidade de domínio (p)?
- [ ] Onde o SINKT se encaixa na arquitetura Jedai + MAIC?
- [ ] Como o modelo lida com questões de diferentes dificuldades?
- [ ] Por que usar dados reais é melhor que dados numéricos abstratos?

---

## Próximos Passos

1. **Experimentar com dados reais:**
   - Substituir dataset simulado por dados de alunos reais
   - Avaliar performance em cenários reais

2. **Implementar GNN:**
   - Integrar Graph Neural Networks
   - Usar estrutura do grafo nas predições

3. **Desenvolver API:**
   - Criar microserviço Jedai_SINKT
   - Implementar endpoints REST

4. **Integrar com MAIC:**
   - Conectar predições do SINKT com intervenções do MAIC
   - Criar fluxo completo de personalização

5. **Expandir banco de questões:**
   - Adicionar mais conceitos de Python
   - Incluir questões de outras linguagens (JavaScript, Java, etc.)

---

## Referências

1. **SINKT Paper:** "Structure-Aware Inductive Knowledge Tracing"
2. **BKT:** Bayesian Knowledge Tracing (modelo base)
3. **GRU:** "Learning Phrase Representations using RNN Encoder-Decoder" (Cho et al., 2014)
4. **PyTorch Documentation:** https://pytorch.org/docs/
5. **Python Official Tutorial:** https://docs.python.org/3/tutorial/

---

## Changelog

### Versão 2.1 (Novembro 2025)
- ✅ Refatoração: dados movidos para arquivos CSV (`data/conceitos.csv`, `data/questoes.csv`, `data/grafo_prerequisitos.csv`)
- ✅ Organização: outputs salvos em pasta dedicada (`outputs/`)
- ✅ Limpeza: todos os emojis removidos do notebook
- ✅ Estrutura mais limpa e profissional

### Versão 2.0 (Novembro 2025)
- ✅ Substituição de dados numéricos por conceitos reais de Python
- ✅ Criação de 15 questões verdadeiras com enunciados completos
- ✅ Grafo de pré-requisitos bem definido (7 relações)
- ✅ Visualizações atualizadas com nomes completos dos conceitos
- ✅ Mini-relatório expandido com exemplos práticos de integração
- ✅ Documentação completa atualizada

### Versão 1.0 (Novembro 2025)
- ✅ Implementação inicial com dados numéricos (K1-K5, Q1-Q10)
- ✅ Pipeline completo: dataset → grafo → embeddings → GRU → predições
- ✅ Visualizações básicas
- ✅ Mini-relatório inicial

---

**Desenvolvido por:** Erick (Time de Dados - 4Linux)  
**Novembro de 2025**
