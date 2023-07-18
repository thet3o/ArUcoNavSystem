"""Navigation ALgorithm Module

This is the navigation algorithm module based on Dijkstra Algorithm

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import math
from queue import PriorityQueue
from data.models import Node

def dijkstra(nodes, start_node, end_node):
    distances = {node: math.inf for node in nodes}
    distances[start_node] = 0
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start_node))
    
    # Find shortest path using dijkstra
    while not pq.empty():
        # find node with smallest distance
        _, current_node = pq.get()
        
        if current_node in visited:
            continue
        
        # node become visited
        visited.add(current_node)
        
        # end node reached
        if current_node == end_node:
            break
        
        # update distances to neighboring nodes
        for neighbor, weight in nodes[current_node].weights.items():
            new_distance = distances[current_node] + int(weight)
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                pq.put((new_distance, neighbor))
                
    # recreate best path
    path = []
    current_node = end_node
    while current_node != start_node:
        path.append(current_node)
        print(current_node)
        current_node = min(nodes[current_node].weights, key=lambda x: distances[x])
    path.append(start_node)
    path.reverse()
    return path