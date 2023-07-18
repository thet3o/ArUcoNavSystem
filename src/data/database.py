"""Database module for ArUcoNavSystem

    This is the module to manage nodes data in sqlite db

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, MetaData, JSON
from .models import Node, NodeInDB
import json
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_path: str):
        engine = create_engine(db_path)
        self.session = sessionmaker(bind=engine)()
        
    def create_node(self, node: Node):
        node.infos = None
        self.session.add(node)
    
    def create_node(self, nodes: list):
        self.session.add_all(nodes)
    
    def get_nodes(self) -> dict:
        nodes = {}
        nodes_db = self.session.query(NodeInDB).all()
        for node in nodes_db:
            nodes[str(node.id)] = Node(node.id, json.loads(node.weights), node.occupied, json.loads(node.infos))
        return nodes
    
    def update_node(self, node_id: int, weights: dict = None, occupied: bool = None, infos: dict = None):
        old_node = self.session.query(NodeInDB).filter(NodeInDB.id == node_id).first()
        self.session.query(NodeInDB).filter(NodeInDB.id == node_id).update({
            NodeInDB.weights : json.dumps(weights) if weights is not None else old_node.weights,
            NodeInDB.occupied : occupied if occupied is not None else old_node.occupied,
            NodeInDB.infos : json.dumps(infos) if infos is not None else {},
        })
        self.session.commit()
        
    def delete_node(self, node: Node):
        return self.session.delete(node)
    