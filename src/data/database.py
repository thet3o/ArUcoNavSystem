import sqlite3
from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, MetaData, JSON


'''connection = sqlite3.connect('database.sqlite')

print(connection.total_changes)

cursor = connection.cursor()

#cursor.execute("CREATE TABLE nodes (id INTEGER PRIMARY KEY, weights JSON DEFAULT('[]'), occupied BOOLEAN, infos JSON DEFAULT('[]'))")

cursor.execute('INSERT INTO nodes VALUES (3, \'{\"1\": 2,\"4\": 5,\"5\": 1}\', 0, \'{\"test\": \"left\"}\')')

connection.commit()'''

from .models import Node, NodeInDB
import json
from sqlalchemy.orm import sessionmaker

#"sqlite:///database.sqlite"

'''class Node:
    def __init__(self, id: str, weights: dict, occupied: bool = False, infos: dict = None):
        self.id = id
        self.weights = weights
        self.occupied = occupied
        self.infos = {} if infos is None else infos
        
    def __str__(self) -> str:
        return json.dumps(self.__dict__)
'''

class Database:
    def __init__(self, db_path: str):
        engine = create_engine(db_path)
        self.session = sessionmaker(bind=engine)()
        
    def create_node(self, node: Node):
        node.infos = json.dumps(node.infos)
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
        
        
    
if __name__ == "__main__":
    
    db = Database('sqlite:///database.sqlite')
    
    node = Node(5, {'3': 5, '2':6})

    db.delete_node(node)
    nodes = db.read_nodes()
    print(db.get_nodes())