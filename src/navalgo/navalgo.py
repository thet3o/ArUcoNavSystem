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
import math
from queue import PriorityQueue

class Node:
    def __init__(self, id: str, weights, occupied: bool = False):
        self.id = id
        self.occupied = occupied
        self.weights = weights
        
def dijkstra(nodes, start_node, end_node):
    distances = {node: math.inf for node in nodes}
    distances[start_node] = 0
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start_node))
    
    # Find shortest path using dijkstra
    while not pq.empty():
        # find node with smallest distance
        #min_node = min((node, distance) for node, distance in distances.items() if node not in visited)[0]
        distance, current_node = pq.get()
        # current node become visited
        #visited.add(min_node)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        if current_node == end_node:
            break
        
        # end node reached break
        #if min_node == end_node:
        #    break
        
        # update distances to neighboring nodes
        for neighbor, weight in nodes[current_node].weights.items():
            new_distance = distances[current_node] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                pq.put((new_distance, neighbor))
                
    # recreate best path
    path = []
    current_node = end_node
    while current_node != start_node:
        print(current_node)
        path.append(current_node)
        current_node = min(nodes[current_node].weights, key=lambda x: distances[x])
    path.append(start_node)
    path.reverse()
    return path
        

def test(start_node):
    n1 = Node("A", False, {
        'B': 1 
    }, {})
    n2 = Node("B", False, {
        'A': 1,
        'C': 2
    }, {})
    n3 = Node("C", False, {
        'B': 2,
        'E': 5,
        'F': 30,
        'D': 6
    }, {})
    n4 = Node("D", False, {
        'C': 6,
        'G': 8
    }, {})
    n5 = Node("E", False, {
        'C': 5
    }, {})
    n6 = Node("F", False, {
        'C': 30,
        'G': 2
    }, {})
    n7 = Node("G", False, {
        'F': 2,
        'D': 8
    }, {})
    
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

    shortest_distances = dijkstra(start_node)
    
    return shortest_distances
        
if __name__ == "__main__":
    
    n1 = Node("A", False, {
        'B': 1
    }, {})
    n2 = Node("B", False, {
        'A': 1,
        'C': 2
    }, {})
    n3 = Node("C", False, {
        'B': 2,
        'E': 5,
        'F': 30,
        'D': 6
    }, {})
    n4 = Node("D", False, {
        'C': 6,
        'G': 8
    }, {})
    n5 = Node("E", False, {
        'C': 5
    }, {})
    n6 = Node("F", False, {
        'C': 30,
        'G': 2
    }, {})
    n7 = Node("G", False, {
        'F': 2,
        'D': 8
    }, {})
    
    nodes = {
        n1.id: n1,
        n2.id: n2,
        n3.id: n3,
        n4.id: n4,
        n5.id: n5,
        n6.id: n6,
        n7.id: n7,
    }
    
    graphs = [n1, n2 ,n3, n4, n5 , n6 , n7 ]
    
    start_node = n7
    end_node = n1
    shortest_distances = dijkstra(graphs, nodes, start_node, end_node)
    
    print(shortest_distances)
    
    for node_id, distance in shortest_distances.items():
        print(f"Shortest distance from {start_node.id} to {node_id} is {distance}")