import json
import networkx as nx
from pyvis.network import Network
import webbrowser
import os
import sys
import math
from collections import defaultdict

# --- Configurações de Cores e Estilo ---
# Paleta de cores baseada nas categorias semânticas do JSON
COLOR_MAP = {
    # Ferramentas e Comandos
    "Ferramentas_e_Comandos": "#FF6B6B",      # Vermelho Suave
    
    # Sistema de Arquivos
    "Sistema_de_Arquivos": "#4ECDC4",         # Turquesa
    
    # Scripting e Automação
    "Scripting_e_Automacao": "#FF9F43",       # Laranja
    
    # Conceitos Fundamentais
    "Conceitos_Fundamentais": "#45B7D1",      # Azul Claro
    
    # Rede e Conectividade
    "Rede_e_Conectividade": "#54A0FF",        # Azul
    
    # Distribuições (mapeado de CONCEITO_TEORICO quando for distribuição)
    "Distribuicoes": "#96CEB4",               # Verde Pálido
    
    # Cores para tipos específicos (fallback)
    "COMANDO": "#FF6B6B",                     # Vermelho Suave
    "SISTEMA_ARQUIVOS": "#4ECDC4",            # Turquesa
    "CONCEITO_TEORICO": "#45B7D1",            # Azul Claro
    "SHELL_SCRIPT": "#FF9F43",                # Laranja
    "REDE": "#54A0FF",                        # Azul
    "FERRAMENTA": "#FF6B6B",                  # Vermelho Suave
    "DEFAULT": "#95A5A6"                      # Cinza (Fallback)
}

# Configurações de visualização das arestas por tipo
EDGE_COLORS = {
    "IS_A": "#2ECC71",        # Verde - para relações de herança/tipo
    "PART_OF": "#3498DB",     # Azul - para relações de composição
    "USE": "#E74C3C",         # Vermelho - para relações de uso
    "RELATED": "#95A5A6",     # Cinza - para relações genéricas
    "RELATED_TO": "#95A5A6",  # Cinza - para relações relacionadas
    "PREREQUISITE": "#F39C12", # Laranja - para pré-requisitos
    "DEFAULT": "#BDC3C7"      # Cinza claro
}

# Configurações de Tamanho
MIN_NODE_SIZE = 10
MAX_NODE_SIZE = 50
SCALING_FACTOR = 2.5

def load_data(filepath):
    """Carrega o JSON do grafo."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar JSON em {filepath}")
        sys.exit(1)

def create_node_tooltip(concept):
    """Gera o texto para o tooltip do nó com informações ricas."""
    nome = concept.get('nome', 'N/A')
    tipo = concept.get('tipo', 'Desconhecido')
    categoria = concept.get('categoria', 'Não categorizado')
    definicao = concept.get('definicao', 'Sem definição.')
    capitulos = concept.get('capitulo_origem', 'N/A')
    grau_entrada = concept.get('grau_entrada', 0)
    grau_saida = concept.get('grau_saida', 0)
    grau_total = concept.get('grau_total', 0)
    nivel = concept.get('nivel_detalhe', 'N/A')
    quality = concept.get('quality_score', 0)
    
    # Formatação HTML para tooltip rico
    tooltip = f"""
    <b><u>{nome}</u></b><br>
    <b>Tipo:</b> {tipo}<br>
    <b>Categoria:</b> {categoria}<br>
    <b>Definição:</b> {definicao}<br>
    <b>Capítulos:</b> {capitulos}<br>
    <b>Nível de Detalhe:</b> {nivel}<br>
    <b>Grau:</b> Entrada: {grau_entrada} | Saída: {grau_saida} | Total: {grau_total}<br>
    <b>Quality Score:</b> {quality:.2f}
    """
    return tooltip.strip()

def create_edge_tooltip(relation):
    """Gera o texto para o tooltip da aresta."""
    rel_type = relation.get('type', 'RELATION')
    confidence = relation.get('confidence', 0)
    explanation = relation.get('explanation', '')
    adicionado = relation.get('adicionado_em_refinamento', False)
    
    # Formatação HTML para tooltip da aresta
    tooltip = f"""
    <b>Tipo:</b> {rel_type}<br>
    <b>Confiança:</b> {confidence:.2f}<br>
    <b>Explicação:</b> {explanation}<br>
    <b>Adicionado em refinamento:</b> {'Sim' if adicionado else 'Não'}
    """
    return tooltip.strip()

def build_graph(data):
    """Constrói o grafo NetworkX com atributos de visualização."""
    G = nx.DiGraph()
    
    # Adicionar Nós
    concepts = data.get('concepts', [])
    print(f"Processando {len(concepts)} conceitos...")
    
    # Estatísticas por categoria
    category_stats = defaultdict(int)
    
    for concept in concepts:
        node_id = concept.get('nome')
        if not node_id:
            continue
            
        node_type = concept.get('tipo', 'DEFAULT')
        categoria = concept.get('categoria', 'DEFAULT')
        
        # Atualizar estatísticas
        category_stats[categoria] += 1
        
        # Determinar cor baseada na categoria (prioridade) ou tipo
        color = COLOR_MAP.get(categoria, COLOR_MAP.get(node_type, COLOR_MAP['DEFAULT']))
        
        # Tooltip rico com HTML
        tooltip_text = create_node_tooltip(concept)
        
        # Determinar o tamanho baseado no grau total e qualidade
        grau_total = concept.get('grau_total', 0)
        quality = concept.get('quality_score', 1.0)
        
        # Nós com maior qualidade e grau são maiores
        size = min(MIN_NODE_SIZE + (grau_total * SCALING_FACTOR * quality), MAX_NODE_SIZE)
        
        # Adicionar borda especial para conceitos de alta qualidade
        border_width = 3 if quality >= 0.9 else 1
        
        G.add_node(node_id, 
                   label=node_id,
                   title=tooltip_text,
                   color=color,
                   group=categoria,
                   value=size,
                   borderWidth=border_width,
                   borderWidthSelected=4,
                   font={'size': 12 if grau_total > 5 else 10, 'bold': grau_total > 10})
    
    # Imprimir estatísticas
    print("\n--- Estatísticas por Categoria ---")
    for cat, count in sorted(category_stats.items()):
        print(f"{cat}: {count} conceitos")
    
    # Adicionar Arestas
    relations = data.get('relations', [])
    print(f"\nProcessando {len(relations)} relações...")
    
    # Estatísticas de tipos de relação
    relation_stats = defaultdict(int)
    
    for rel in relations:
        source = rel.get('source')
        target = rel.get('target')
        rel_type = rel.get('type', 'RELATED')
        confidence = rel.get('confidence', 0.5)
        
        # Atualizar estatísticas
        relation_stats[rel_type] += 1
        
        # Verificar se os nós existem no grafo
        if source in G and target in G:
            # Tooltip rico para aresta
            tooltip_text = create_edge_tooltip(rel)
            
            # Cor da aresta baseada no tipo
            edge_color = EDGE_COLORS.get(rel_type, EDGE_COLORS['DEFAULT'])
            
            # Largura da aresta baseada na confiança
            width = 1 + (confidence * 3)
            
            # Opacidade baseada na confiança
            opacity = 0.3 + (confidence * 0.7)
            
            # Adicionar aresta com estilo
            G.add_edge(source, target, 
                       label=rel_type,
                       title=tooltip_text,
                       color=edge_color,
                       width=width,
                       arrows='to',
                       opacity=opacity,
                       font={'size': 8, 'color': edge_color})
    
    # Imprimir estatísticas de relações
    print("\n--- Estatísticas de Relações ---")
    for rel_type, count in sorted(relation_stats.items()):
        print(f"{rel_type}: {count} relações")
    
    return G

def calculate_sizes(G):
    """Função mantida para compatibilidade, mas os tamanhos já são calculados em build_graph."""
    pass

def main():
    # Caminhos absolutos para garantir funcionamento
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input do arquivo concepts_graph.json (voltando duas pastas para chegar na raiz)
    input_path = os.path.join(base_dir, "..", "..", "json", "concepts_graph.json")
    
    # Output na mesma pasta de visualização
    output_dir = base_dir
    output_path = os.path.join(output_dir, "interactive_graph.html")
    
    print("--- Gerador de Visualização de Grafo de Conceitos Linux ---")
    print(f"Arquivo de entrada: {input_path}")
    print(f"Arquivo de saída: {output_path}")
    
    # 1. Carregar Dados
    data = load_data(input_path)
    
    # Exibir metadados
    metadata = data.get('metadata', {})
    print(f"\n--- Metadados do Grafo ---")
    print(f"Método: {metadata.get('method', 'N/A')}")
    print(f"Versão: {metadata.get('versao', 'N/A')}")
    print(f"Data de Processamento: {metadata.get('data_processamento', 'N/A')}")
    print(f"Total de Conceitos: {metadata.get('total_conceitos', 0)}")
    print(f"Total de Relações: {metadata.get('total_relacoes', 0)}")
    
    # 2. Construir Grafo NetworkX
    G = build_graph(data)
    
    print(f"\nGrafo construído: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas.")
    
    # 3. Configurar PyVis
    # Configuração inicial com opções avançadas
    net = Network(
        height="95vh", 
        width="100%", 
        bgcolor="#1a1a1a",  # Fundo escuro para melhor contraste
        font_color="#ffffff", 
        select_menu=True,  # Habilitar menu de seleção
        filter_menu=True,  # Habilitar menu de filtro
        cdn_resources='remote'
    )
    
    # Configurar opções de física específicas para grafos direcionados
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08,
          "damping": 0.4,
          "avoidOverlap": 0.1
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based",
        "timestep": 0.22
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "hideEdgesOnDrag": true,
        "hideNodesOnDrag": true,
        "navigationButtons": true,
        "keyboard": true
      },
      "layout": {
        "hierarchical": {
          "enabled": false
        }
      },
      "clusters": {
        "clusterNodeProperties": {
          "borderWidth": 3,
          "borderWidthSelected": 5
        }
      }
    }
    """)
    
    # Importar do NetworkX
    net.from_nx(G)
    
    # 4. Salvar e Abrir
    print(f"\nSalvando visualização em: {output_path}")
    try:
        net.save_graph(output_path)
        print("✓ Arquivo salvo com sucesso!")
        
        # Ler o HTML gerado para adicionar legendas
        with open(output_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Adicionar legendas após o body
        legend_html = """
        <div style="position: fixed; top: 10px; right: 10px; background: rgba(255,255,255,0.9); padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); z-index: 1000;">
            <h4 style="margin: 0 0 10px 0;">Legendas</h4>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #FF6B6B; margin-right: 5px; border: 1px solid #ccc;"></div>
                <span>Ferramentas e Comandos</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #4ECDC4; margin-right: 5px; border: 1px solid #ccc;"></div>
                <span>Sistema de Arquivos</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #FF9F43; margin-right: 5px; border: 1px solid #ccc;"></div>
                <span>Scripting e Automação</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #45B7D1; margin-right: 5px; border: 1px solid #ccc;"></div>
                <span>Conceitos Fundamentais</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #54A0FF; margin-right: 5px; border: 1px solid #ccc;"></div>
                <span>Rede e Conectividade</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #96CEB4; margin-right: 5px; border: 1px solid #ccc;"></div>
                <span>Hardware e Periféricos</span>
            </div>
        </div>
        """
        
        # Inserir as legendas após a tag body
        html_content = html_content.replace('<body>', '<body>' + legend_html)
        
        # Salvar o HTML modificado
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Tentar abrir no navegador
        abs_path = os.path.abspath(output_path)
        webbrowser.open(f"file://{abs_path}")
        print("✓ Abrindo visualização no navegador...")
        
        # Estatísticas finais
        print("\n--- Resumo da Visualização ---")
        print(f"✓ Nós: {G.number_of_nodes()}")
        print(f"✓ Arestas: {G.number_of_edges()}")
        
        # Corrigir acesso aos nós para obter categorias
        categories = set()
        for node_id in net.nodes:
            if 'group' in net.get_node(node_id):
                categories.add(net.get_node(node_id)['group'])
        print(f"✓ Categorias: {len(categories)}")
        
        # Corrigir acesso às arestas para obter tipos de relação
        relation_types = set()
        for edge in net.edges:
            if 'label' in edge:
                relation_types.add(edge['label'])
        print(f"✓ Tipos de relação: {len(relation_types)}")
        
    except Exception as e:
        print(f"✗ Erro ao salvar/abrir arquivo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
