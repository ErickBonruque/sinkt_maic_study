# SINKT and MAIC

Guia de estudos e anotações sobre SINKT (knowledge tracing indutivo com grafos) e MAIC
(salas de aula com agentes), com implementações e simulações feitas a partir dos artigos.

## Conteúdo

| Pasta | O que tem |
|---|---|
| `sinkt_colab/` | Implementação base do SINKT com um conjunto pequeno de conceitos e questões de Python |
| `sinkt_correcoes/` | Versão revisada da implementação e anotações de revisão |
| `sinkt_simulation/` | Simulação de alunos e conceitos com atualização de domínio (BKT) |
| `simulacao_estudantes/` | Pipeline em 5 notebooks: perfis, alunos sintéticos, interações, respostas via LLM, treino do SINKT |
| `sinkt_extraction_graph/` | Extração de conceitos e relações de um PDF e construção do grafo com agentes |
| `maic_simulation/` | Notas e comparação entre MAIC e SINKT |

## Sobre os dados

Os notebooks de `simulacao_estudantes/` e `sinkt_extraction_graph/` estão sem saídas e sem os arquivos
de dados: a versão original usava como entrada um material didático de terceiros, que não pode ser
redistribuído. Para rodar, coloque um PDF próprio (ou de licença livre) em
`sinkt_extraction_graph/<variante>/pdf/` e execute os notebooks na ordem; os arquivos em `output/` e
`data/` são gerados de novo.
