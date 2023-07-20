"""Simulator module

This is the simulator module where the graph of the path is visualized

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import networkx as nx
from data.models import Node
import matplotlib.pyplot as plt

# build graph
def build_graph(nodes: dict, path):
    G = nx.Graph()
    #for id, val in nodes.items():
    #    graph.add_node(id, node=val)
    #    for k, v in val.weights.items():
    #        graph.add_edge(id, k, weight=v)
    
    for k, node in nodes.items():
        #print(nodes.items())
        G.add_node(node.to_json()['id'], **node.to_json(), label=node.to_json()['id'])
            
    for k, node in nodes.items():
        for k, weight in node.weights.items():
            G.add_edge(node.id, k)
    
            
    #edge_colors = ['lime' if e in path_edges else 'black' for e in G.edges]
    
    return G

def show_graph(graph: nx.Graph, edge_colors):
    nx.draw(graph, with_labels=True, edge_color=edge_colors, width=2)
    plt.show()