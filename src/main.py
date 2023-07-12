from navalgo.navalgo import Node, dijkstra
from simulator.simulator import build_graph, show_graph, show_moving_robot

if __name__ == '__main__':
    nodes = {
        'A': Node('A', {'B': 1}),
        'B': Node('B', {'A': 1,'C': 2}),
        'C': Node('C', {'B': 2,'E': 5,'F': 1,'D': 6}),
        'D': Node('D', {'C': 6,'G': 8}),
        'E': Node('E', {'C': 5}),
        'F': Node('F', {'C': 1,'G': 2}),
        'G': Node('G', {'F': 2,'D': 8}),
    }
    #print(graphd.edges)
    graph = [v for k, v in nodes.items()]
    #show_graph(graphd)
    show_moving_robot(graph, ['A', 'B', 'C', 'E'])
    path = dijkstra(nodes, 'A', 'G')
    print(path)
    graphd, edge_colors = build_graph(nodes, path)
    show_graph(graphd, edge_colors)