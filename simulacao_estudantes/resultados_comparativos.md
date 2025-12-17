# Relatório Comparativo de Resultados - Projeto SINKT

## 🎯 Métricas de Desempenho

### Treinamento vs Validação vs Teste

| Métrica | Treinamento | Validação | Teste |
|---------|-------------|-----------|-------|
| **Loss Final** | 0.4502 | 0.5275 | 0.4913 |
| **Loss Inicial** | 0.6778 | 0.7000 | - |
| **Melhor Loss** | 0.4392 | 0.5181 | - |
| **AUC** | - | 0.7914 | 0.8218 |
| **Accuracy** | - | 0.7795 | 0.7869 |
| **F1-Score** | - | 0.8097 | 0.7360 |
| **Precision** | - | - | 0.6996 |
| **Recall** | - | - | 0.7763 |

### 📈 Melhorias Durante o Treinamento

- **Melhoria no Loss de Treinamento**: 33.58%
- **Melhoria no Loss de Validação**: 24.65%
- **Número de Épocas Treinadas**: 34
- **Melhor AUC de Validação**: 0.7999

---

## 👥 Análise de Evolução por Perfil de Aluno

### Evolução de Domínio e Accuracy

| Perfil | Nº Alunos | Accuracy (%) | Evolução Domínio (%) | Evolução Individual Média (%) |
|--------|-----------|--------------|----------------------|-------------------------------|
| Equilibrado | 30 | 44.09 | 0.49 | 21.00 ± 81.86 |
| Cuidadoso | 20 | 43.16 | 0.37 | 14.88 ± 104.07 |
| Intuitivo | 10 | 38.18 | 0.83 | 42.70 ± 119.12 |
| Lógico | 10 | 32.08 | -0.38 | -14.19 ± 94.96 |
| Aprendiz Rápido | 20 | 51.64 | 0.6706 | 0.6755 | 0.73 | 43.75 ± 80.20 |
| Com Dificuldades | 10 | 24.65 | 0.1766 | 0.1809 | 2.48 | 76.87 ± 182.72 |


## 📋 Conclusões

1. **Desempenho do Modelo**: O modelo SINKT alcançou AUC de 0.8218 nos dados de teste, demonstrando boa capacidade de predição.

2. **Evolução dos Alunos**: A análise por perfil revela diferentes padrões de aprendizagem, com evoluções variando entre -0.38% e 2.48% dependendo do perfil.

3. **Potencial de Personalização**: Os resultados sugerem que abordagens personalizadas considerando o perfil do aluno podem otimizar o processo de aprendizagem.
