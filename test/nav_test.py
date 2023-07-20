import unittest
from src.navigation.navigation import Node, dijkstra

class NavTest(unittest.TestCase):
    
    def __init__(self, methodName: str = "runTest") -> None:
        self.nodes = {
        'A': Node('A', {'B': 1}),
        'B': Node('B', {'A': 1,'C': 2}),
        'C': Node('C', {'B': 2,'E': 5,'F': 1,'D': 6}),
        'D': Node('D', {'C': 6,'G': 8}),
        'E': Node('E', {'C': 5}),
        'F': Node('F', {'C': 1,'G': 2}),
        'G': Node('G', {'F': 2,'D': 8}),
        }
        super().__init__(methodName)
    
    def test_shortest_path(self):
        self.assertEqual(dijkstra(self.nodes, 'A', 'G'), ['A', 'B', 'C', 'F', 'G'],)