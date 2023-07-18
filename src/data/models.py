"""Models file

This is the file where the models for the software are stored

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import json
from sqlalchemy import Column, Integer, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base


class Node:
    def __init__(self, id: str, weights: dict, occupied: bool = False, infos: dict = None):
        self.id = id
        self.weights = weights
        self.occupied = occupied
        self.infos = {} if infos is None else infos
        
    def __str__(self) -> str:
        return json.dumps(self.__dict__)
    
class NodeInDB(declarative_base()):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True)
    
    weights = Column(JSON, nullable=False)
    occupied = Column(Boolean, default=False)
    infos = Column(JSON, nullable=True)