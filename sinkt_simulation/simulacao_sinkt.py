"""
Simulação do Modelo SINKT - Evolução de Domínio de Conceitos
Baseado nas fórmulas de BKT (Bayesian Knowledge Tracing)

Autor: Sistema de Simulação
Data: 2025-11-16
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuração de fonte para português
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

# Configuração de estilo
sns.set_style("whitegrid")
sns.set_palette("husl")

# Parâmetros do modelo BKT
ALPHA = 0.3  # Taxa de aprendizado (quando acerta)
BETA = 0.1   # Taxa de esquecimento (quando erra)

# Configuração da simulação
ALUNOS = ['A', 'B', 'C', 'D', 'E']
CONCEITOS = ['K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K07', 'K08']
NUM_INTERACOES = 10

# Probabilidades iniciais de domínio (p₀) para cada aluno
# Valores entre 0.1 e 0.5 para simular diferentes níveis iniciais
P_INICIAL = {
    'A': 0.3,  # Aluno médio
    'B': 0.5,  # Aluno com conhecimento prévio bom
    'C': 0.2,  # Aluno com dificuldades
    'D': 0.4,  # Aluno bom
    'E': 0.15  # Aluno com muitas dificuldades
}

# Perfis de desempenho para gerar padrões realistas
# Cada conceito tem uma dificuldade relativa
DIFICULDADE_CONCEITO = {
    'K01': 0.7,  # Conceito fácil (alta chance de acerto)
    'K02': 0.6,  # Fácil-médio
    'K03': 0.5,  # Médio
    'K04': 0.4,  # Médio-difícil
    'K05': 0.3,  # Difícil
    'K06': 0.5,  # Médio
    'K07': 0.6,  # Fácil-médio
    'K08': 0.4   # Médio-difícil
}

def gerar_resultado_tentativa(p_dominio, dificuldade_conceito, variabilidade=0.15):
    """
    Gera resultado de uma tentativa (1=acerto, 0=erro) baseado em:
    - p_dominio: probabilidade atual de domínio do aluno
    - dificuldade_conceito: facilidade do conceito (0-1)
    - variabilidade: ruído aleatório
    
    Returns:
        1 (acerto) ou 0 (erro)
    """
    # Probabilidade de acerto combina domínio do aluno e dificuldade do conceito
    prob_acerto = (p_dominio * 0.6) + (dificuldade_conceito * 0.4)
    
    # Adiciona variabilidade (ruído)
    prob_acerto += np.random.uniform(-variabilidade, variabilidade)
    prob_acerto = np.clip(prob_acerto, 0.0, 1.0)
    
    # Gera resultado
    return 1 if np.random.random() < prob_acerto else 0

def atualizar_probabilidade(p_atual, resultado, alpha=ALPHA, beta=BETA):
    """
    Atualiza a probabilidade de domínio usando fórmulas BKT
    
    Args:
        p_atual: probabilidade atual de domínio
        resultado: 1 (acerto) ou 0 (erro)
        alpha: taxa de aprendizado
        beta: taxa de esquecimento
    
    Returns:
        Nova probabilidade de domínio
    """
    if resultado == 1:  # Acerto
        p_novo = p_atual + alpha * (1 - p_atual)
    else:  # Erro
        p_novo = p_atual * (1 - beta)
    
    return np.clip(p_novo, 0.0, 1.0)

def simular_aprendizado():
    """
    Simula o processo de aprendizado para todos os alunos e conceitos
    
    Returns:
        DataFrame com histórico completo de interações
    """
    dados = []
    
    for aluno in ALUNOS:
        p_inicial_aluno = P_INICIAL[aluno]
        
        for conceito in CONCEITOS:
            dificuldade = DIFICULDADE_CONCEITO[conceito]
            
            # Inicializa probabilidade de domínio para este conceito
            # Varia um pouco em relação ao p_inicial do aluno
            p_dominio = p_inicial_aluno + np.random.uniform(-0.1, 0.1)
            p_dominio = np.clip(p_dominio, 0.05, 0.95)
            
            # Registra estado inicial (interação 0)
            dados.append({
                'aluno': aluno,
                'conceito': conceito,
                'interacao': 0,
                'resultado': None,
                'p_antes': None,
                'p_depois': p_dominio
            })
            
            # Simula 10 interações
            for i in range(1, NUM_INTERACOES + 1):
                p_antes = p_dominio
                
                # Gera resultado da tentativa
                resultado = gerar_resultado_tentativa(p_dominio, dificuldade)
                
                # Atualiza probabilidade de domínio
                p_dominio = atualizar_probabilidade(p_dominio, resultado)
                
                # Registra dados
                dados.append({
                    'aluno': aluno,
                    'conceito': conceito,
                    'interacao': i,
                    'resultado': resultado,
                    'p_antes': p_antes,
                    'p_depois': p_dominio
                })
    
    return pd.DataFrame(dados)

def criar_planilha_excel(df, caminho_saida):
    """
    Cria planilha Excel formatada com múltiplas abas
    """
    with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
        # Aba 1: Dados completos
        df_completo = df.copy()
        df_completo.to_excel(writer, sheet_name='Dados Completos', index=False)
        
        # Aba 2: Resumo por aluno e conceito (apenas interações com resultado)
        df_interacoes = df[df['resultado'].notna()].copy()
        df_resumo = df_interacoes.groupby(['aluno', 'conceito']).agg({
            'resultado': ['sum', 'count', 'mean'],
            'p_antes': 'first',
            'p_depois': 'last'
        }).reset_index()
        df_resumo.columns = ['aluno', 'conceito', 'acertos', 'tentativas', 
                             'taxa_acerto', 'p_inicial', 'p_final']
        df_resumo['ganho'] = df_resumo['p_final'] - df_resumo['p_inicial']
        df_resumo.to_excel(writer, sheet_name='Resumo por Conceito', index=False)
        
        # Aba 3: Matriz de resultados (aluno x conceito)
        for aluno in ALUNOS:
            df_aluno = df[(df['aluno'] == aluno) & (df['resultado'].notna())]
            matriz = df_aluno.pivot_table(
                index='interacao', 
                columns='conceito', 
                values='resultado',
                aggfunc='first'
            )
            matriz.to_excel(writer, sheet_name=f'Aluno {aluno}')
        
        # Aba 4: Evolução de p (aluno x conceito)
        for aluno in ALUNOS:
            df_aluno = df[df['aluno'] == aluno]
            matriz_p = df_aluno.pivot_table(
                index='interacao', 
                columns='conceito', 
                values='p_depois',
                aggfunc='first'
            )
            matriz_p.to_excel(writer, sheet_name=f'Evolução p - {aluno}')
        
        # Aba 5: Estatísticas gerais
        stats = []
        for aluno in ALUNOS:
            df_aluno = df[(df['aluno'] == aluno) & (df['resultado'].notna())]
            stats.append({
                'aluno': aluno,
                'total_tentativas': len(df_aluno),
                'total_acertos': df_aluno['resultado'].sum(),
                'taxa_acerto_geral': df_aluno['resultado'].mean(),
                'p_inicial_medio': df[df['aluno'] == aluno]['p_depois'].iloc[0],
                'p_final_medio': df[(df['aluno'] == aluno) & (df['interacao'] == NUM_INTERACOES)]['p_depois'].mean()
            })
        df_stats = pd.DataFrame(stats)
        df_stats['ganho_medio'] = df_stats['p_final_medio'] - df_stats['p_inicial_medio']
        df_stats.to_excel(writer, sheet_name='Estatísticas Gerais', index=False)

def criar_visualizacoes(df, pasta_saida):
    """
    Cria todas as visualizações solicitadas
    """
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(exist_ok=True, parents=True)
    
    # 1. Evolução individual por aluno (todos os conceitos)
    for aluno in ALUNOS:
        fig, ax = plt.subplots(figsize=(12, 6))
        df_aluno = df[df['aluno'] == aluno]
        
        for conceito in CONCEITOS:
            df_conceito = df_aluno[df_aluno['conceito'] == conceito]
            ax.plot(df_conceito['interacao'], df_conceito['p_depois'], 
                   marker='o', label=conceito, linewidth=2, markersize=6)
        
        ax.set_xlabel('Interação', fontsize=12, fontweight='bold')
        ax.set_ylabel('Probabilidade de Domínio (p)', fontsize=12, fontweight='bold')
        ax.set_title(f'Evolução do Domínio - Aluno {aluno}', fontsize=14, fontweight='bold')
        ax.legend(loc='best', ncol=2)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        plt.tight_layout()
        plt.savefig(pasta_saida / f'evolucao_aluno_{aluno}.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # 2. Evolução média por conceito (todos os alunos)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for conceito in CONCEITOS:
        df_conceito = df[df['conceito'] == conceito]
        media_por_interacao = df_conceito.groupby('interacao')['p_depois'].mean()
        ax.plot(media_por_interacao.index, media_por_interacao.values, 
               marker='s', label=conceito, linewidth=2.5, markersize=7)
    
    ax.set_xlabel('Interação', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probabilidade Média de Domínio (p)', fontsize=12, fontweight='bold')
    ax.set_title('Evolução Média do Domínio por Conceito', fontsize=14, fontweight='bold')
    ax.legend(loc='best', ncol=2)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.05, 1.05)
    plt.tight_layout()
    plt.savefig(pasta_saida / 'evolucao_media_conceitos.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Heatmap de domínio final (alunos x conceitos)
    df_final = df[df['interacao'] == NUM_INTERACOES]
    matriz_final = df_final.pivot_table(index='aluno', columns='conceito', 
                                        values='p_depois', aggfunc='first')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(matriz_final, annot=True, fmt='.3f', cmap='RdYlGn', 
                vmin=0, vmax=1, cbar_kws={'label': 'Probabilidade de Domínio'},
                linewidths=0.5, ax=ax)
    ax.set_title('Domínio Final por Aluno e Conceito', fontsize=14, fontweight='bold')
    ax.set_xlabel('Conceito', fontsize=12, fontweight='bold')
    ax.set_ylabel('Aluno', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(pasta_saida / 'heatmap_dominio_final.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Comparação de ganho de aprendizado
    df_inicial = df[df['interacao'] == 0]
    df_final = df[df['interacao'] == NUM_INTERACOES]
    
    ganhos = []
    for aluno in ALUNOS:
        p_inicial = df_inicial[df_inicial['aluno'] == aluno]['p_depois'].mean()
        p_final = df_final[df_final['aluno'] == aluno]['p_depois'].mean()
        ganhos.append({
            'aluno': aluno,
            'p_inicial': p_inicial,
            'p_final': p_final,
            'ganho': p_final - p_inicial
        })
    
    df_ganhos = pd.DataFrame(ganhos)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(ALUNOS))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, df_ganhos['p_inicial'], width, label='Inicial', alpha=0.8)
    bars2 = ax.bar(x + width/2, df_ganhos['p_final'], width, label='Final', alpha=0.8)
    
    ax.set_xlabel('Aluno', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probabilidade Média de Domínio', fontsize=12, fontweight='bold')
    ax.set_title('Comparação: Domínio Inicial vs Final por Aluno', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(ALUNOS)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 1.0)
    
    # Adiciona valores nas barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(pasta_saida / 'comparacao_inicial_final.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Taxa de acerto ao longo do tempo
    df_interacoes = df[df['resultado'].notna()]
    taxa_acerto = df_interacoes.groupby('interacao')['resultado'].mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(taxa_acerto.index, taxa_acerto.values, marker='o', 
           linewidth=3, markersize=8, color='#2E86AB')
    ax.fill_between(taxa_acerto.index, taxa_acerto.values, alpha=0.3, color='#2E86AB')
    
    ax.set_xlabel('Interação', fontsize=12, fontweight='bold')
    ax.set_ylabel('Taxa de Acerto', fontsize=12, fontweight='bold')
    ax.set_title('Evolução da Taxa de Acerto Geral', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.0)
    
    # Adiciona linha de tendência
    z = np.polyfit(taxa_acerto.index, taxa_acerto.values, 1)
    p = np.poly1d(z)
    ax.plot(taxa_acerto.index, p(taxa_acerto.index), "--", 
           color='red', linewidth=2, label='Tendência', alpha=0.7)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(pasta_saida / 'taxa_acerto_evolucao.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """
    Função principal que executa toda a simulação
    """
    print("=" * 60)
    print("SIMULAÇÃO SINKT - EVOLUÇÃO DE DOMÍNIO DE CONCEITOS")
    print("=" * 60)
    print()
    
    # Define seed para reprodutibilidade
    np.random.seed(42)
    
    print("1. Gerando dados de simulação...")
    df = simular_aprendizado()
    print(f"   ✓ {len(df)} registros gerados")
    print()
    
    print("2. Criando planilha Excel...")
    caminho_excel = '/home/ubuntu/sinkt_simulation/Simulacao_SINKT_Alunos_Conceitos.xlsx'
    criar_planilha_excel(df, caminho_excel)
    print(f"   ✓ Planilha salva: {caminho_excel}")
    print()
    
    print("3. Gerando visualizações...")
    pasta_graficos = '/home/ubuntu/sinkt_simulation/graficos'
    criar_visualizacoes(df, pasta_graficos)
    print(f"   ✓ Gráficos salvos em: {pasta_graficos}")
    print()
    
    print("4. Estatísticas gerais:")
    df_interacoes = df[df['resultado'].notna()]
    print(f"   - Total de interações: {len(df_interacoes)}")
    print(f"   - Taxa de acerto geral: {df_interacoes['resultado'].mean():.2%}")
    print(f"   - Probabilidade inicial média: {df[df['interacao']==0]['p_depois'].mean():.3f}")
    print(f"   - Probabilidade final média: {df[df['interacao']==NUM_INTERACOES]['p_depois'].mean():.3f}")
    print()
    
    print("=" * 60)
    print("SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    
    return df

if __name__ == "__main__":
    df_resultado = main()
