# -*- coding: utf-8 -*-
"""
Conceitos e Questões Reais de Programação Python
Para o projeto SINKT Base Individual
"""

# ============================================================================
# CONCEITOS DE PROGRAMAÇÃO PYTHON
# ============================================================================

CONCEITOS = {
    'variaveis_tipos': {
        'nome': 'Variáveis e Tipos de Dados',
        'descricao': 'Declaração de variáveis, tipos básicos (int, float, str, bool)',
        'nivel': 1,
        'prerequisitos': []
    },
    'operadores': {
        'nome': 'Operadores Aritméticos e Lógicos',
        'descricao': 'Operações matemáticas (+, -, *, /), comparação (==, !=, <, >), lógicos (and, or, not)',
        'nivel': 1,
        'prerequisitos': ['variaveis_tipos']
    },
    'condicionais': {
        'nome': 'Estruturas Condicionais (if/elif/else)',
        'descricao': 'Tomada de decisões com if, elif, else',
        'nivel': 2,
        'prerequisitos': ['variaveis_tipos', 'operadores']
    },
    'loops': {
        'nome': 'Estruturas de Repetição (for/while)',
        'descricao': 'Loops for e while, range(), break, continue',
        'nivel': 2,
        'prerequisitos': ['variaveis_tipos', 'operadores']
    },
    'funcoes': {
        'nome': 'Funções',
        'descricao': 'Definição de funções, parâmetros, return, escopo',
        'nivel': 3,
        'prerequisitos': ['condicionais', 'loops']
    }
}

# ============================================================================
# QUESTÕES REAIS POR CONCEITO
# ============================================================================

QUESTOES = {
    # ========== VARIÁVEIS E TIPOS DE DADOS ==========
    'Q001': {
        'conceito': 'variaveis_tipos',
        'enunciado': 'Qual é o tipo de dado da variável `x = 10`?',
        'opcoes': ['A) str', 'B) int', 'C) float', 'D) bool'],
        'resposta_correta': 'B',
        'dificuldade': 'facil'
    },
    'Q002': {
        'conceito': 'variaveis_tipos',
        'enunciado': 'Qual código converte o número 42 para string?',
        'opcoes': ['A) int(42)', 'B) str(42)', 'C) float(42)', 'D) bool(42)'],
        'resposta_correta': 'B',
        'dificuldade': 'facil'
    },
    'Q003': {
        'conceito': 'variaveis_tipos',
        'enunciado': 'O que acontece ao executar: `nome = "Ana"; idade = 25; print(nome + idade)`?',
        'opcoes': [
            'A) Imprime "Ana25"',
            'B) Imprime 25',
            'C) Gera erro (TypeError)',
            'D) Imprime "Ana 25"'
        ],
        'resposta_correta': 'C',
        'dificuldade': 'medio'
    },
    
    # ========== OPERADORES ==========
    'Q004': {
        'conceito': 'operadores',
        'enunciado': 'Qual é o resultado de `10 // 3` em Python?',
        'opcoes': ['A) 3.33', 'B) 3', 'C) 4', 'D) 3.0'],
        'resposta_correta': 'B',
        'dificuldade': 'facil'
    },
    'Q005': {
        'conceito': 'operadores',
        'enunciado': 'Qual é o resultado de `5 > 3 and 2 < 1`?',
        'opcoes': ['A) True', 'B) False', 'C) Erro', 'D) None'],
        'resposta_correta': 'B',
        'dificuldade': 'medio'
    },
    'Q006': {
        'conceito': 'operadores',
        'enunciado': 'O que retorna `not (10 == 10 or 5 > 7)`?',
        'opcoes': ['A) True', 'B) False', 'C) None', 'D) Erro'],
        'resposta_correta': 'B',
        'dificuldade': 'medio'
    },
    
    # ========== CONDICIONAIS ==========
    'Q007': {
        'conceito': 'condicionais',
        'enunciado': 'Qual será a saída do código?\n```python\nx = 15\nif x > 10:\n    print("A")\nelif x > 5:\n    print("B")\nelse:\n    print("C")\n```',
        'opcoes': ['A) A', 'B) B', 'C) C', 'D) AB'],
        'resposta_correta': 'A',
        'dificuldade': 'facil'
    },
    'Q008': {
        'conceito': 'condicionais',
        'enunciado': 'Qual código verifica se um número é par?',
        'opcoes': [
            'A) if num % 2 == 0:',
            'B) if num / 2 == 0:',
            'C) if num % 2 == 1:',
            'D) if num // 2 == 0:'
        ],
        'resposta_correta': 'A',
        'dificuldade': 'facil'
    },
    'Q009': {
        'conceito': 'condicionais',
        'enunciado': 'O que imprime o código?\n```python\nnota = 7\nif nota >= 7:\n    if nota >= 9:\n        print("A")\n    else:\n        print("B")\nelse:\n    print("C")\n```',
        'opcoes': ['A) A', 'B) B', 'C) C', 'D) Nada'],
        'resposta_correta': 'B',
        'dificuldade': 'medio'
    },
    
    # ========== LOOPS ==========
    'Q010': {
        'conceito': 'loops',
        'enunciado': 'Quantas vezes o loop executa?\n```python\nfor i in range(5):\n    print(i)\n```',
        'opcoes': ['A) 4 vezes', 'B) 5 vezes', 'C) 6 vezes', 'D) Infinitas'],
        'resposta_correta': 'B',
        'dificuldade': 'facil'
    },
    'Q011': {
        'conceito': 'loops',
        'enunciado': 'O que imprime o código?\n```python\nfor i in range(2, 6):\n    print(i, end=" ")\n```',
        'opcoes': ['A) 2 3 4 5', 'B) 2 3 4 5 6', 'C) 0 1 2 3 4 5', 'D) 1 2 3 4 5'],
        'resposta_correta': 'A',
        'dificuldade': 'medio'
    },
    'Q012': {
        'conceito': 'loops',
        'enunciado': 'O que faz o `break` em um loop?',
        'opcoes': [
            'A) Pula para a próxima iteração',
            'B) Interrompe o loop completamente',
            'C) Reinicia o loop',
            'D) Não faz nada'
        ],
        'resposta_correta': 'B',
        'dificuldade': 'facil'
    },
    
    # ========== FUNÇÕES ==========
    'Q013': {
        'conceito': 'funcoes',
        'enunciado': 'Qual é a saída do código?\n```python\ndef soma(a, b):\n    return a + b\nresultado = soma(3, 5)\nprint(resultado)\n```',
        'opcoes': ['A) 8', 'B) 35', 'C) None', 'D) Erro'],
        'resposta_correta': 'A',
        'dificuldade': 'facil'
    },
    'Q014': {
        'conceito': 'funcoes',
        'enunciado': 'O que acontece se uma função não tem `return`?',
        'opcoes': [
            'A) Retorna 0',
            'B) Retorna None',
            'C) Gera erro',
            'D) Retorna True'
        ],
        'resposta_correta': 'B',
        'dificuldade': 'medio'
    },
    'Q015': {
        'conceito': 'funcoes',
        'enunciado': 'Qual é a saída?\n```python\ndef multiplicar(x, y=2):\n    return x * y\nprint(multiplicar(5))\n```',
        'opcoes': ['A) 5', 'B) 10', 'C) 7', 'D) Erro'],
        'resposta_correta': 'B',
        'dificuldade': 'medio'
    }
}

# ============================================================================
# GRAFO DE PRÉ-REQUISITOS
# ============================================================================

GRAFO_PREREQUISITOS = [
    ('variaveis_tipos', 'operadores'),
    ('variaveis_tipos', 'condicionais'),
    ('operadores', 'condicionais'),
    ('variaveis_tipos', 'loops'),
    ('operadores', 'loops'),
    ('condicionais', 'funcoes'),
    ('loops', 'funcoes')
]

# ============================================================================
# MAPEAMENTO QUESTÃO -> CONCEITO
# ============================================================================

def get_questao_conceito_map():
    """Retorna mapeamento de questão para conceito"""
    return {q_id: q_data['conceito'] for q_id, q_data in QUESTOES.items()}

def get_conceitos_list():
    """Retorna lista de IDs de conceitos"""
    return list(CONCEITOS.keys())

def get_questoes_list():
    """Retorna lista de IDs de questões"""
    return list(QUESTOES.keys())

def get_questoes_por_conceito(conceito_id):
    """Retorna lista de questões de um conceito específico"""
    return [q_id for q_id, q_data in QUESTOES.items() if q_data['conceito'] == conceito_id]
