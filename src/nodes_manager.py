"""Nodes Manager

This is a small interface to interact with the nodes storage(sqlite db)

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import PySimpleGUI as pyg
from data.database import Database
from data.models import NodeInDB
import json


db = Database('sqlite:///database.sqlite')
nodes = [v for k, v in db.get_nodes().items()]
weights = {}
nodes_list_layout = [
    [
        pyg.Text('Nodes List', expand_x=True, justification='center', font=['Arial Bold', 20]),
    ],
    [
        pyg.Listbox(
            values=[node.id for node in nodes], enable_events=True, key='NODES LIST', size=(30, 28)
        )
    ]
]

update_add_node = [
    [
        pyg.Text('Node View', expand_x=True, justification='center', font=['Arial Bold', 20]),
    ],
    [
        pyg.Text('Node ID'),
        pyg.In(size=(3,1), enable_events=True, key="ID FIELD"),
    ],
    [
        pyg.Checkbox('Node occupied?', size=(20,5), key="OCCUPIED FIELD", enable_events=True),
    ],
    [
        pyg.Text('Weights:'),
        pyg.In(size=(3,1), key='WEIGHT NODE ID', tooltip='Node Id'), pyg.In(size=(3,1), key='WEIGHT NODE WEIGHT', tooltip='Node Weight'),
    ],
    [
        pyg.Button('ADD/UP WEIGHT', key='ADDUP WEIGHT NODE', auto_size_button=True, enable_events=True),
        pyg.Button('DELETE WEIGHT', key='DELETE WEIGHT NODE', auto_size_button=True,enable_events=True)
    ],
    [
        pyg.Listbox(
            values=[], enable_events=True, key='WEIGHT NODE LIST', size=(30,20), auto_size_text=True, expand_x=True, expand_y=True
        ),
    ],
]

layout = [
    [
        pyg.Column(nodes_list_layout),
        pyg.VSeparator(),
        pyg.Column(update_add_node)
    ],
    [
        pyg.Button('Save2Db', key='SAVE2DB', enable_events=True),
        pyg.Button('NEW NODE', key='NEW NODE', enable_events=True),
        pyg.Button('ADD NODE', key='ADD NODE', enable_events=True),
    ]
]

window = pyg.Window('Nodes Manager', layout=layout, element_justification='center')

id_field = None

while True:
    event, values = window.read()
    
    if event == 'Exit' or event == pyg.WIN_CLOSED:
        break
    
    if event == 'NODES LIST':
        
        id_field = int(''.join(map(str, window.Element('NODES LIST').Widget.curselection())))
        checked = next((x.occupied for x in nodes if x.id == id_field), None)
        print(checked)
        print(id_field)
        weights = nodes[id_field].weights
        window.Element('WEIGHT NODE LIST').Update([f'Node: {k},Metric:{v}' for k,v in nodes[id_field].weights.items()])
        window.Element('OCCUPIED FIELD').Update(nodes[id_field].occupied)
        window.Element('ID FIELD').Update(nodes[id_field].id)
    elif event == 'ADDUP WEIGHT NODE':
        #weights.update({values['WEIGHT NODE ID'] : values['WEIGHT NODE WEIGHT']})
        weight_id = values['WEIGHT NODE ID']
        weight_value = values['WEIGHT NODE WEIGHT']
        weights[weight_id] = weight_value
        nodes[id_field].weights = weights
        window.Element('WEIGHT NODE LIST').Update([f'Node: {k},Metric:{v}' for k,v in weights.items()])
    elif event == 'WEIGHT NODE LIST':
        id_field = int(''.join(map(str, window.Element('WEIGHT NODE LIST').Widget.curselection())))
        id, weight = ''.join(values['WEIGHT NODE LIST']).strip().replace(' ', '').split(',')
        _, id = id.split(':')
        _, weight = weight.split(':')
        window.Element('WEIGHT NODE ID').Update(id)
        window.Element('WEIGHT NODE WEIGHT').Update(weight)
        print(f'{id} {weight}')
    elif event == 'SAVE2DB':
        for node in nodes:
            db.update_node(node.id, node.weights, node.occupied)
    elif event == 'OCCUPIED FIELD':
        nodes[id_field].occupied = values['OCCUPIED FIELD']
    elif event == 'NEW NODE':
        window.Element('WEIGHT NODE ID').Update('')
        window.Element('WEIGHT NODE WEIGHT').Update('')
        window.Element('WEIGHT NODE LIST').Update([])
        window.Element('ID FIELD').Update('')
        window.Element('OCCUPIED FIELD').Update(False)
    elif event == 'ADD NODE':
        id_field = len(nodes) - 1
        new_node = NodeInDB(id=values['ID FIELD'],weights=json.dumps({}),occupied=values['OCCUPIED FIELD'], infos=json.dumps({}))
        nodes.append(new_node)
        db.create_node([new_node])
        nodes = [v for k, v in db.get_nodes().items()]
        window.Element('NODES LIST').Update([node.id for node in nodes])
    elif event == 'ID FIELD':
        id_field = int(values['ID FIELD'])
window.close()