"""Simulator module

This is the simulator module where every function written here is used to simulate,
or move in the real world the robot

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import networkx as nx
from navigation.navigation import Node
import matplotlib.pyplot as plt

# build graph
def build_graph(nodes: dict, path):
    graph = nx.Graph()
    for id, val in nodes.items():
        graph.add_node(id, node=val)
        for k, v in val.weights.items():
            graph.add_edge(id, k, weight=v)
            
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    
            
    edge_colors = ['lime' if e in path_edges else 'black' for e in graph.edges]
    
    return graph, edge_colors

def show_graph(graph: nx.Graph, edge_colors):
    nx.draw(graph, with_labels=True, edge_color=edge_colors, width=2)
    plt.show()