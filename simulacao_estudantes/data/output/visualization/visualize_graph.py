import json
import networkx as nx
from pyvis.network import Network
import webbrowser
import os
import sys
import math
from collections import defaultdict, Counter

# --- Configurações de Cores e Estilo ---
# Paleta de cores para tipos de questões
QUESTION_TYPE_COLORS = {
    "definition": "#FF6B6B",      # Vermelho Suave
    "application": "#4ECDC4",     # Turquesa
    "multiple_choice": "#45B7D1", # Azul Claro
    "analysis": "#FF9F43",        # Laranja
}

# Paleta de cores para dificuldade
DIFFICULTY_COLORS = {
    "easy": "#2ECC71",      # Verde
    "medium": "#F39C12",    # Amarelo/Laranja
    "hard": "#E74C3C",      # Vermelho
}

# Paleta de cores para níveis de Bloom
BLOOM_COLORS = {
    "remember": "#9B59B6",     # Roxo
    "understand": "#3498DB",   # Azul
    "apply": "#1ABC9C",        # Verde-água
    "analyze": "#E67E22",      # Laranja
}

# Paleta de cores para tipos de conceito
CONCEPT_TYPE_COLORS = {
    "COMANDO": "#FF6B6B",
    "SISTEMA_ARQUIVOS": "#4ECDC4",
    "CONCEITO_TEORICO": "#45B7D1",
    "SHELL_SCRIPT": "#FF9F43",
    "REDE": "#54A0FF",
    "FERRAMENTA": "#FF6B6B",
    "DEFAULT": "#95A5A6"
}

# Configurações de Tamanho
MIN_NODE_SIZE = 10
MAX_NODE_SIZE = 50
SCALING_FACTOR = 2.0

def load_data(filepath):
    """Carrega o JSON do grafo de questões."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar JSON em {filepath}")
        sys.exit(1)

def create_question_tooltip(question):
    """Gera o texto para o tooltip da questão."""
    q_id = question.get('id', 'N/A')
    q_type = question.get('type', 'Desconhecido')
    difficulty = question.get('difficulty', 'N/A')
    bloom = question.get('bloom', 'N/A')
    concept = question.get('concept_name', 'N/A')
    text = question.get('text', 'Sem texto.')
    answer = question.get('answer', 'Sem resposta.')
    related = question.get('related_concepts', [])
    keywords = question.get('keywords', [])
    
    # Formatação HTML para tooltip rico
    tooltip = f"""
    <b><u>Questão: {q_id}</u></b><br>
    <b>Tipo:</b> {q_type}<br>
    <b>Dificuldade:</b> {difficulty}<br>
    <b>Taxonomia de Bloom:</b> {bloom}<br>
    <b>Conceito Principal:</b> {concept}<br>
    <hr>
    <b>Questão:</b><br>{text}<br>
    <hr>
    <b>Resposta:</b><br>{answer}<br>
    <hr>
    <b>Conceitos Relacionados:</b> {', '.join(related) if related else 'Nenhum'}<br>
    <b>Palavras-chave:</b> {', '.join(keywords) if keywords else 'Nenhuma'}
    """
    return tooltip.strip()

def create_concept_tooltip(concept_questions):
    """Gera o texto para o tooltip do conceito agregado."""
    concept_name = concept_questions['name']
    concept_type = concept_questions['type']
    total_questions = concept_questions['total']
    type_dist = concept_questions['type_distribution']
    diff_dist = concept_questions['difficulty_distribution']
    bloom_dist = concept_questions['bloom_distribution']
    
    tooltip = f"""
    <b><u>Conceito: {concept_name}</u></b><br>
    <b>Tipo:</b> {concept_type}<br>
    <b>Total de Questões:</b> {total_questions}<br>
    <hr>
    <b>Distribuição por Tipo:</b><br>
    """
    for qtype, count in type_dist.items():
        tooltip += f"• {qtype}: {count}<br>"
    
    tooltip += "<hr><b>Distribuição por Dificuldade:</b><br>"
    for diff, count in diff_dist.items():
        tooltip += f"• {diff}: {count}<br>"
    
    tooltip += "<hr><b>Distribuição por Bloom:</b><br>"
    for bloom, count in bloom_dist.items():
        tooltip += f"• {bloom}: {count}<br>"
    
    return tooltip.strip()

def build_question_graph(data):
    """Constrói o grafo de questões com conceitos como nós intermediários."""
    G = nx.DiGraph()
    
    questions = data.get('questions', [])
    print(f"Processando {len(questions)} questões...")
    
    # Agrupar questões por conceito
    concept_groups = defaultdict(list)
    for q in questions:
        concept_id = q.get('concept_id')
        if concept_id:
            concept_groups[concept_id].append(q)
    
    # Adicionar nós de conceitos agregados
    concept_nodes = {}
    for concept_id, concept_questions_list in concept_groups.items():
        if concept_questions_list:
            first_q = concept_questions_list[0]
            concept_name = first_q.get('concept_name', concept_id)
            concept_type = first_q.get('concept_type', 'DEFAULT')
            
            # Calcular distribuições
            type_dist = Counter([q.get('type') for q in concept_questions_list])
            diff_dist = Counter([q.get('difficulty') for q in concept_questions_list])
            bloom_dist = Counter([q.get('bloom') for q in concept_questions_list])
            
            concept_data = {
                'name': concept_name,
                'type': concept_type,
                'total': len(concept_questions_list),
                'type_distribution': dict(type_dist),
                'difficulty_distribution': dict(diff_dist),
                'bloom_distribution': dict(bloom_dist),
                'questions': concept_questions_list
            }
            
            # Cor baseada no tipo de conceito
            color = CONCEPT_TYPE_COLORS.get(concept_type, CONCEPT_TYPE_COLORS['DEFAULT'])
            
            # Tamanho baseado no número de questões
            size = min(MIN_NODE_SIZE + (len(concept_questions_list) * SCALING_FACTOR), MAX_NODE_SIZE)
            
            G.add_node(f"concept_{concept_id}",
                      label=concept_name,
                      title=create_concept_tooltip(concept_data),
                      color=color,
                      group=concept_type,
                      value=size,
                      node_type='concept',
                      shape='box')
            
            concept_nodes[concept_id] = f"concept_{concept_id}"
    
    # Adicionar nós de questões e conectar aos conceitos
    question_types = Counter()
    difficulties = Counter()
    bloom_levels = Counter()
    
    for question in questions:
        q_id = question.get('id')
        concept_id = question.get('concept_id')
        q_type = question.get('type')
        difficulty = question.get('difficulty')
        bloom = question.get('bloom')
        
        if not q_id or not concept_id:
            continue
        
        # Atualizar contadores
        question_types[q_type] += 1
        difficulties[difficulty] += 1
        bloom_levels[bloom] += 1
        
        # Cor baseada no tipo de questão
        color = QUESTION_TYPE_COLORS.get(q_type, QUESTION_TYPE_COLORS['definition'])
        
        # Borda baseada na dificuldade
        border_color = DIFFICULTY_COLORS.get(difficulty, DIFFICULTY_COLORS['medium'])
        
        # Tooltip rico
        tooltip_text = create_question_tooltip(question)
        
        G.add_node(q_id,
                  label=f"Q{q_id.split('_q')[-1]}",
                  title=tooltip_text,
                  color=color,
                  group=q_type,
                  value=15,
                  borderWidth=3,
                  borderColor=border_color,
                  node_type='question',
                  shape='ellipse')
        
        # Conectar questão ao conceito
        if concept_id in concept_nodes:
            G.add_edge(q_id, concept_nodes[concept_id],
                      color='#BDC3C7',
                      width=1,
                      arrows='to',
                      title='Pertence ao conceito')
        
        # Conectar a conceitos relacionados
        related_concepts = question.get('related_concepts', [])
        for related in related_concepts:
            # Encontrar o ID do conceito relacionado
            for cid, cname in concept_nodes.items():
                if G.nodes[cname]['label'] == related:
                    G.add_edge(q_id, cname,
                              color='#95A5A6',
                              width=1,
                              dashes=True,
                              arrows='to',
                              title='Conceito relacionado',
                              opacity=0.5)
                    break
    
    # Imprimir estatísticas
    print("\n--- Estatísticas das Questões ---")
    print(f"Total de conceitos com questões: {len(concept_nodes)}")
    print("\nDistribuição por tipo:")
    for qtype, count in question_types.most_common():
        print(f"  {qtype}: {count}")
    print("\nDistribuição por dificuldade:")
    for diff, count in difficulties.most_common():
        print(f"  {diff}: {count}")
    print("\nDistribuição por Bloom:")
    for bloom, count in bloom_levels.most_common():
        print(f"  {bloom}: {count}")
    
    return G

def main():
    # Caminhos absolutos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input do arquivo questions_graph.json (voltando duas pastas para chegar na raiz)
    input_path = os.path.join(base_dir, "..", "..", "json", "questions_graph.json")
    
    # Output na mesma pasta de visualização
    output_dir = base_dir
    output_path = os.path.join(output_dir, "questions_graph.html")
    
    print("--- Gerador de Visualização do Grafo de Questões ---")
    print(f"Arquivo de entrada: {input_path}")
    print(f"Arquivo de saída: {output_path}")
    
    # 1. Carregar Dados
    data = load_data(input_path)
    
    # Exibir metadados
    metadata = data.get('metadata', {})
    print(f"\n--- Metadados do Grafo de Questões ---")
    print(f"Versão: {metadata.get('version', 'N/A')}")
    print(f"Descrição: {metadata.get('description', 'N/A')}")
    print(f"Total de Questões: {metadata.get('total_questions', 0)}")
    print(f"Total de Conceitos: {metadata.get('total_concepts', 0)}")
    print(f"Média de Questões por Conceito: {metadata.get('avg_questions_per_concept', 0):.2f}")
    
    # 2. Construir Grafo NetworkX
    G = build_question_graph(data)
    
    print(f"\nGrafo construído: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas.")
    
    # 3. Configurar PyVis
    net = Network(
        height="95vh",
        width="100%",
        bgcolor="#1a1a1a",
        font_color="#ffffff",
        select_menu=True,
        filter_menu=True,
        cdn_resources='remote'
    )
    
    # Configurar opções de física
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "centralGravity": 0.01,
          "springLength": 150,
          "springConstant": 0.08,
          "damping": 0.4,
          "avoidOverlap": 0.5
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
      "nodes": {
        "font": {
          "size": 12
        }
      }
    }
    """)
    
    # Importar do NetworkX
    net.from_nx(G)
    
    # 4. Salvar e Adicionar Legendas
    print(f"\nSalvando visualização em: {output_path}")
    try:
        net.save_graph(output_path)
        print("✓ Arquivo salvo com sucesso!")
        
        # Ler e modificar o HTML para adicionar legendas
        with open(output_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Legendas para tipos de questão
        legend_html = """
        <div style="position: fixed; top: 10px; right: 10px; background: rgba(255,255,255,0.95); padding: 15px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 1000; max-width: 300px;">
            <h4 style="margin: 0 0 10px 0; color: #333;">Tipos de Questão</h4>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #FF6B6B; margin-right: 8px; border: 1px solid #ccc; border-radius: 3px;"></div>
                <span style="color: #333;">Definição</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #4ECDC4; margin-right: 8px; border: 1px solid #ccc; border-radius: 3px;"></div>
                <span style="color: #333;">Aplicação</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #45B7D1; margin-right: 8px; border: 1px solid #ccc; border-radius: 3px;"></div>
                <span style="color: #333;">Múltipla Escolha</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #FF9F43; margin-right: 8px; border: 1px solid #ccc; border-radius: 3px;"></div>
                <span style="color: #333;">Análise</span>
            </div>
            
            <h4 style="margin: 15px 0 10px 0; color: #333;">Dificuldade (Borda)</h4>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background: white; border: 3px solid #2ECC71; margin-right: 8px; border-radius: 3px;"></div>
                <span style="color: #333;">Fácil</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background: white; border: 3px solid #F39C12; margin-right: 8px; border-radius: 3px;"></div>
                <span style="color: #333;">Médio</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background: white; border: 3px solid #E74C3C; margin-right: 8px; border-radius: 3px;"></div>
                <span style="color: #333;">Difícil</span>
            </div>
            
            <h4 style="margin: 15px 0 10px 0; color: #333;">Forma dos Nós</h4>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background: #95A5A6; margin-right: 8px; border-radius: 50%;"></div>
                <span style="color: #333;">Questão</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 15px; background: #95A5A6; margin-right: 8px; border-radius: 3px;"></div>
                <span style="color: #333;">Conceito</span>
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
        
        # Contar tipos de nós
        question_nodes = sum(1 for n in G.nodes() if G.nodes[n].get('node_type') == 'question')
        concept_nodes_count = sum(1 for n in G.nodes() if G.nodes[n].get('node_type') == 'concept')
        print(f"✓ Questões: {question_nodes}")
        print(f"✓ Conceitos: {concept_nodes_count}")
        
    except Exception as e:
        print(f"✗ Erro ao salvar/abrir arquivo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
