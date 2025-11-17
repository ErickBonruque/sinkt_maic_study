# Proposta de Integração Técnica: Jedai ↔ SINKT

**Data da Proposta:** 16 de novembro de 2025

## 1. Visão Geral

Esta proposta descreve um fluxo técnico para integrar o modelo de rastreamento de conhecimento SINKT (utilizando a lógica BKT para a atualização de domínio) com a plataforma Jedai. O objetivo é permitir que o sistema atualize a probabilidade de domínio de um aluno sobre um conceito específico em tempo real, logo após a conclusão de uma atividade avaliativa (como um quiz).

Essa integração é fundamental para a personalização do aprendizado, pois permite que o Jedai adapte o conteúdo, recomende atividades e forneça feedback com base no nível de conhecimento atual e preciso de cada aluno.

## 2. Fluxo de Integração

O processo de integração é iniciado no frontend (plataforma Jedai) e processado pelo backend, que hospeda a lógica do SINKT. O fluxo pode ser resumido nas seguintes etapas:

1.  **Ação do Usuário:** O aluno responde a uma questão ou completa um quiz associado a um conceito específico na plataforma Jedai.
2.  **Evento Disparado:** O frontend da aplicação dispara um evento, como `quiz.completed`, contendo os dados da interação.
3.  **Requisição à API:** O frontend envia uma requisição HTTP (POST) para um endpoint dedicado no backend.
4.  **Processamento no Backend:** O backend recebe a requisição, recupera o estado de conhecimento atual do aluno, aplica a fórmula de atualização do SINKT/BKT e persiste o novo estado no banco de dados.
5.  **Resposta:** O backend retorna uma resposta de sucesso, confirmando que o domínio do aluno foi atualizado.

### Diagrama do Fluxo

![Diagrama de Sequência - Integração SINKT-Jedai](/home/ubuntu/sinkt_simulation/graficos/diagrama_integracao.png)
*Figura 1: Fluxo de integração entre o frontend Jedai e o backend SINKT para atualização de domínio em tempo real.*

## 3. Especificação Técnica

### Endpoint

-   **URL:** `/sinkt/update`
-   **Método:** `POST`
-   **Content-Type:** `application/json`

### Payload da Requisição (Request Body)

O corpo da requisição deve conter as seguintes informações:

| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| `user_id` | String | Sim | Identificador único do aluno. |
| `concept_id` | String | Sim | Identificador único do conceito avaliado. |
| `result` | Integer | Sim | Resultado da interação: **1** para acerto, **0** para erro. |

**Exemplo de Payload:**
```json
{
  "user_id": "aluno_C",
  "concept_id": "K04",
  "result": 0
}
```

### Resposta da API (Response Body)

Em caso de sucesso, a API retorna um status `200 OK` com o seguinte corpo:

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `status` | String | Indica o resultado da operação (e.g., "success"). |
| `user_id` | String | O ID do aluno que foi atualizado. |
| `concept_id` | String | O ID do conceito que foi atualizado. |
| `old_p` | Float | A probabilidade de domínio *antes* da atualização. |
| `new_p` | Float | A probabilidade de domínio *após* a atualização. |

**Exemplo de Resposta:**
```json
{
  "status": "success",
  "user_id": "aluno_C",
  "concept_id": "K04",
  "old_p": 0.45,
  "new_p": 0.405
}
```

## 4. Exemplo de Implementação (Backend com Python/Flask)

A seguir, um exemplo simplificado de como o endpoint `/sinkt/update` poderia ser implementado usando o framework Flask em Python.

```python
from flask import Flask, request, jsonify

# --- Configuração do Modelo ---
ALPHA = 0.3  # Taxa de aprendizado
BETA = 0.1   # Taxa de esquecimento/erro

# --- Simulação de um Banco de Dados ---
# Em um ambiente real, isso seria uma tabela em um banco de dados relacional ou NoSQL.
# Estrutura: db[user_id][concept_id] = p_dominio
db = {
    "aluno_A": {"K01": 0.5, "K02": 0.7},
    "aluno_C": {"K04": 0.45}
}

# --- Aplicação Flask ---
app = Flask(__name__)

def atualizar_probabilidade(p_atual, resultado):
    """Aplica a fórmula de atualização BKT."""
    if resultado == 1:
        return p_atual + ALPHA * (1 - p_atual)
    else:
        return p_atual * (1 - BETA)

@app.route("/sinkt/update", methods=["POST"])
def handle_sinkt_update():
    data = request.get_json()

    # 1. Validação do payload
    if not all(k in data for k in ["user_id", "concept_id", "result"]):
        return jsonify({"error": "Payload incompleto"}), 400

    user_id = data["user_id"]
    concept_id = data["concept_id"]
    result = data["result"]

    # 2. Recuperar o estado de conhecimento atual
    # Se o aluno ou conceito não existir, inicializa com um valor padrão (ex: 0.2)
    p_atual = db.setdefault(user_id, {}).setdefault(concept_id, 0.2)

    # 3. Calcular o novo estado de conhecimento
    p_novo = atualizar_probabilidade(p_atual, result)

    # 4. Persistir o novo estado
    db[user_id][concept_id] = p_novo

    # 5. Retornar a resposta
    response = {
        "status": "success",
        "user_id": user_id,
        "concept_id": concept_id,
        "old_p": p_atual,
        "new_p": p_novo
    }
    return jsonify(response), 200

if __name__ == "__main__":
    # Para fins de teste, execute com: flask run
    app.run(debug=True, port=5001)

```

## 5. Considerações Finais

-   **Segurança:** Em um ambiente de produção, o endpoint deve ser protegido por autenticação e autorização para garantir que apenas a plataforma Jedai possa enviar atualizações e que os dados dos alunos sejam mantidos em sigilo.
-   **Escalabilidade:** Para um grande volume de interações, o acesso ao banco de dados deve ser otimizado. O uso de um cache (como Redis) para armazenar os estados de conhecimento mais recentes pode reduzir a latência.
-   **Inicialização:** A lógica para definir a probabilidade inicial de um conceito para um aluno (`p_inicial`) precisa ser bem definida. Pode ser um valor padrão, ou um valor derivado do desempenho do aluno em conceitos pré-requisito.
