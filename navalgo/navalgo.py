"""Navigation Alogorithm Module
"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'


''' first num = zone type 1 must pass here
    Fake codes
        000 start point
        101 run1
        002 run2
        003 entrance
        005 bar
        
        path 000 -> 001 -> 003 -> 005
'''

import heapq


class Node:
    def __init__(self, id: str, occupied: bool, weights):
        self.id = id
        self.occupied = occupied
        self.weights = weights
        
def dijkstra(start_node):
    distances = {node.id: float('inf') for node in graph}
    distances[start_node.id] = 0
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if a shorter path to current_node has already been found
        if current_distance > distances[current_node.id]:
            continue

        for neighbor_id, weight in current_node.weights.items():
            neighbor = nodes[neighbor_id]
            distance = current_distance + weight
            if distance < distances[neighbor.id]:
                distances[neighbor.id] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances
        
if __name__ == "__main__":
    
    n1 = Node("A", False, {'B': 1 })
    n2 = Node("B", False, {
        'A': 1,
        'C': 2
    })
    n3 = Node("C", False, {
        'B': 2,
        'E': 5,
        'F': 30,
        'D': 6
    })
    n4 = Node("D", False, {
        'C': 6,
        'G': 8
    })
    n5 = Node("E", False, {
        'C': 5
    })
    n6 = Node("F", False, {
        'C': 30,
        'G': 2
    })
    n7 = Node("G", False, {
        'F': 2,
        'D': 8
    })
    
    nodes = {
        n1.id: n1,
        n2.id: n2,
        n3.id: n3,
        n4.id: n4,
        n5.id: n5,
        n6.id: n6,
        n7.id: n7,
    }
    
    graph = [n1, n2 ,n3, n4, n5 , n6 , n7 ]
    
    start_node = n1
    shortest_distances = dijkstra(start_node)
    
    for node_id, distance in shortest_distances.items():
        print(f"Shortest distance from {start_node.id} to {node_id} is {distance}")