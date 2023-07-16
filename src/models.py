import json
from json import JSONEncoder, JSONDecoder

class Node:
    def __init__(self, id: str, weights: dict, occupied: bool = False):
        self.id = id
        self.weights = weights
        self.occupied = occupied
        
    def __str__(self) -> str:
        return json.dumps(self.__dict__)