import json
import networkx as nx
from pyvis.network import Network
import webbrowser
import os
import sys

# --- Configurações de Cores e Estilo ---
# Paleta de cores para diferentes tipos de conceitos
COLOR_MAP = {
    "COMANDO": "#FF6B6B",           # Vermelho Suave
    "SISTEMA_ARQUIVOS": "#4ECDC4",  # Turquesa
    "CONCEITO_TEORICO": "#45B7D1",  # Azul Claro
    "DISTRIBUICAO": "#96CEB4",      # Verde Pálido
    "KERNEL": "#FFCC5C",            # Amarelo
    "PROCESSO": "#FF9F43",          # Laranja
    "PERMISSAO": "#D6A2E8",         # Lilás
    "REDE": "#54A0FF",              # Azul
    "DEFAULT": "#95A5A6"            # Cinza (Fallback)
}

# Configurações de Tamanho
MIN_NODE_SIZE = 15
MAX_NODE_SIZE = 45
SCALING_FACTOR = 3

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
    """Gera o texto para o tooltip do nó."""
    nome = concept.get('nome', 'N/A')
    tipo = concept.get('tipo', 'Desconhecido')
    definicao = concept.get('definicao', 'Sem definição.')
    capitulos = concept.get('capitulo_origem', 'N/A')
    
    # Formatação texto simples para garantir compatibilidade
    tooltip = f"Nome: {nome}\nTipo: {tipo}\nDefinição: {definicao}\nCapítulos: {capitulos}"
    return tooltip

def create_edge_tooltip(relation):
    """Gera o texto para o tooltip da aresta."""
    # Apenas o tipo da relação conforme solicitado
    return relation.get('type', 'RELATION')

def build_graph(data):
    """Constrói o grafo NetworkX com atributos de visualização."""
    G = nx.DiGraph()
    
    # Adicionar Nós
    concepts = data.get('concepts', [])
    print(f"Processando {len(concepts)} conceitos...")
    
    ignored_nodes = set()
    
    for concept in concepts:
        node_id = concept.get('nome')
        if not node_id:
            continue
            
        node_type = concept.get('tipo', 'DEFAULT')
        
        # Filtrar nós de ruído
        if node_type == "NOISE":
            ignored_nodes.add(node_id)
            continue
            
        color = COLOR_MAP.get(node_type, COLOR_MAP['DEFAULT'])
        # Tooltip agora é texto simples
        tooltip_text = create_node_tooltip(concept)
        
        G.add_node(node_id, 
                   label=node_id,
                   title=tooltip_text,
                   color=color,
                   group=node_type) 
    
    if ignored_nodes:
        print(f"Ignorados {len(ignored_nodes)} nós do tipo 'NOISE'.")

    # Adicionar Arestas
    relations = data.get('relations', [])
    print(f"Processando {len(relations)} relações...")
    
    for rel in relations:
        source = rel.get('source')
        target = rel.get('target')
        rel_type = rel.get('type', 'RELATED')
        
        # Verificar se os nós existem no grafo (filtra automaticamente conexões com NOISE)
        if source in G and target in G:
            # Tooltip agora é apenas o tipo
            tooltip_text = create_edge_tooltip(rel)
            G.add_edge(source, target, 
                       label=rel_type,
                       title=tooltip_text,
                       arrows='to')
    
    return G

def calculate_sizes(G):
    """Calcula tamanhos dos nós baseado no grau (conexões)."""
    degrees = dict(G.degree())
    if not degrees:
        return
        
    # Normalização simples para tamanho
    for node in G.nodes():
        degree = degrees[node]
        # Tamanho base + fator * grau, limitado ao MAX_NODE_SIZE
        size = min(MIN_NODE_SIZE + (degree * SCALING_FACTOR), MAX_NODE_SIZE)
        G.nodes[node]['value'] = size # 'value' é usado pelo PyVis para escalar

def main():
    # Caminhos absolutos para garantir funcionamento
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "output", "enhanced_graph.json")
    output_path = os.path.join(base_dir, "output", "interactive_graph.html")
    
    print("--- Gerador de Visualização de Grafo SINKT ---")
    
    # 1. Carregar Dados
    data = load_data(input_path)
    
    # 2. Construir Grafo NetworkX
    G = build_graph(data)
    
    # 3. Calcular Tamanhos (Hubs maiores)
    calculate_sizes(G)
    
    print(f"Grafo construído: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas.")
    
    # 4. Configurar PyVis
    # Remover select_menu e filter_menu conforme solicitado
    net = Network(height="90vh", width="100%", bgcolor="#ffffff", font_color="black", select_menu=False, filter_menu=False, cdn_resources='remote')
    
    # Importar do NetworkX
    net.from_nx(G)
    
    # 5. Configurar Física (Force Atlas 2 Based é ótimo para grafos densos)
    net.force_atlas_2based(
        gravity=-50,
        central_gravity=0.01,
        spring_length=100,
        spring_strength=0.08,
        damping=0.4,
        overlap=0
    )
    
    # Adicionar botões de controle
    net.show_buttons(filter_=['physics'])
    
    # 6. Salvar e Abrir
    print(f"Salvando visualização em: {output_path}")
    try:
        net.save_graph(output_path)
        print("Arquivo salvo com sucesso!")
        
        # Tentar abrir no navegador
        # Usar file:// para garantir compatibilidade local
        abs_path = os.path.abspath(output_path)
        webbrowser.open(f"file://{abs_path}")
        print("Tentando abrir no navegador...")
        
    except Exception as e:
        print(f"Erro ao salvar/abrir arquivo: {e}")

if __name__ == "__main__":
    main()
