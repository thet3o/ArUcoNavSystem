from navalgo.navalgo import Node
from simulator.simulator import build_graph, show_graph, show_moving_robot

if __name__ == '__main__':
    nodes = [
        Node('A', {'B': 1}),
        Node('B', {'A': 1,'C': 2}),
        Node('C', {'B': 2,'E': 5,'F': 30,'D': 6}),
        Node('D', {'C': 6,'G': 8}),
        Node('E', {'C': 5}),
        Node('F', {'C': 30,'G': 2}),
        Node('G', {'F': 2,'D': 8}),
    ]
    graph = build_graph(nodes)
    #show_graph(graph)
    show_moving_robot(graph, ['A', 'B', 'C', 'E'])