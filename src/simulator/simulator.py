"""Simulator module

This is the simulator module where every function written here is used to simulate,
or move in the real world the robot

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import networkx as nx
from navalgo.navalgo import Node
import matplotlib.pyplot as plt


def build_graph(nodes: list):
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node.id, node=node)
        for k, v in node.weights.items():
            graph.add_edge(node.id, k, weight=v)
    return graph

def show_graph(graph: nx.Graph):
    nx.draw(graph, with_labels=True)
    plt.show()
    
def show_moving_robot(graph, path: list):
    
    current_node = 'A'
    
    while current_node != path[-1]:
        next_node_index = (path.index(current_node)+1)
        print(f'Moving from {current_node} to {path[next_node_index]}')
        current_node = path[next_node_index]