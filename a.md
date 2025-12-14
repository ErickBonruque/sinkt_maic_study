# Validação dos conceitos SINKT (Extração + Estratégias)

Dando continuidade à validação da extração de conceitos, fiz algumas alterações arquiteturais importantes no projeto.

Para otimizar os testes e comparar estratégias de custo vs performance, dividi a execução em dois diretórios distintos: **`codex`** (focado em potência) e **`master`** (focado em eficiência).

### Versão CODEX:
Nesta versão, foquei na qualidade máxima de "Recall" (descoberta de relações).
*   **Mudança de Escopo (Agentes):** Inicialmente, a task previa **8 agentes** independentes. Porém, durante os testes, percebi que a orquestração completa de 8 agentes aumentaria drasticamente o tempo de execução e a complexidade do grafo neste momento. Por falta de tempo hábil e para garantir uma entrega funcional, optei por implementar **4 agentes super-especializados** primeiro:
    1.  **Cleaner:** Filtra alucinações iniciais.
    2.  **Expert:** Valida a verdade técnica e pedagógica.
    3.  **Analyst:** Garante a consistência topológica.
    4.  **Judge:** Consolida os votos e toma a decisão final.

Nós: 216
Arestas: 260

### Versão MASTER:
Esta é a versão "Low Cost".
*   **Estratégia:** Em vez de múltiplas chamadas de agentes, utilizei um **Mega-Prompt**.
*   **Simulação:** Aqui consegui simular a "Mesa Redonda" completa com as **8 personas** planejadas (Professor, Engenheiro, Cético, Topólogo, etc.) em uma única chamada de API via processamento em batch. É menos granular, mas muito mais rápido e barato.

Nós: 226
Arestas: 174

## Comparativo

*   **Densidade:** O **Codex** gerou um grafo mais denso (+25% de arestas).
*   **Limpeza:** O **Master** foi mais conservador, resultando em um grafo mais esparso.