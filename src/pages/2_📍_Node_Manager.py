from calibration.calibration import read_charuco, calibrate_camera
from aruco.aruco import detect_marker
import numpy as np
from streamlit_webrtc import webrtc_streamer
import streamlit as st
import streamlit.components.v1 as components
import cv2
import av
import glob
import plotly
from streamlit_extras.metric_cards import style_metric_cards
import copy
import plotly.graph_objs as go
from data.database import Database
import matplotlib.pyplot as plt
import networkx as nx
from pyvis import network as net
from simulator.simulator import build_graph
import pandas as pd
from st_aggrid import AgGrid
from data.models import Node, NodeInDB
import json

st.title('Node Manager')

mcol1, mcol2 = st.columns(2, gap='medium')

db = Database('sqlite:///database.sqlite')
nodes = db.get_nodes()
graph = build_graph(nodes, ['0', '4'])


st.session_state.nodes = nodes

def id_callback():
    node_ids = [k for k, node in st.session_state.nodes.items()]
    try:
        st.session_state.weight_node_id = next(iter(nodes[str(st.session_state.node_id)].weights))
        st.session_state.weight_node_metric = nodes[str(st.session_state.node_id)].weights[st.session_state.weight_node_id]
    except KeyError:
        pass
    
def occupied_callback():
    nodes[str(node_id)].occupied = st.session_state.node_occupied
    db = Database('sqlite:///database.sqlite')
    db.update_node(node_id, occupied=st.session_state.node_occupied)
    
def weights_callback():
    node_id = st.session_state.weights.replace('Node:', '')
    st.session_state.weight_node_id = node_id
    st.session_state.weight_node_metric = nodes[str(st.session_state.node_id)].weights[node_id]
    
def weight_node_callback():
    nodes[str(st.session_state.node_id)].weights[st.session_state.weight_node_id] = st.session_state.weight_node_metric
    db.update_node(node_id, weights=nodes[str(st.session_state.node_id)].weights)
    
def delete_weight_callback():    
     del nodes[str(st.session_state.node_id)].weights[st.session_state.weight_node_id]
     db.update_node(st.session_state.node_id, weights=nodes[str(st.session_state.node_id)].weights)
     
def delete_node_callback():
    db.delete_node(nodes[str(st.session_state.node_id)].id)
    
nodejson = [node.to_json() for k, node in nodes.items()]

df = pd.DataFrame(nodejson)

fig, ax = plt.subplots()
pos = nx.spring_layout(graph, seed=42)
nx.draw(graph, with_labels=True, width=2, ax=ax, pos=pos)

mcol1.pyplot(fig)
mcol2.dataframe(df)

with st.container():
    st.subheader('Node Editor')
    node_id = st.number_input('Node ID', on_change=id_callback, key='node_id', step=1)
    try:
        occupied = st.checkbox('Occupied',
                           nodes[str(node_id)].occupied if nodes[str(node_id)].occupied is not None else False,
                           on_change=occupied_callback, key='node_occupied')
        delete_node = st.button('DELETE NODE', on_click=delete_node_callback, use_container_width=True)
        weights = st.selectbox('Weights: ',
                               [f'Node:{node}' for  node, weight in nodes[str(node_id)].weights.items()],
                               on_change=weights_callback, key='weights')
        with st.container():
            col1, col2 = st.columns(2)
            weight_node_id = col1.text_input('Weight Node ID', key='weight_node_id', on_change=weight_node_callback)
            weight_node_metric = col2.text_input('Weight Node Metric', key='weight_node_metric', on_change=weight_node_callback)
            weight_node_delete = st.button('DELETE WEIGHT NODE', use_container_width=True, on_click=delete_weight_callback)
            
    except KeyError:
        add_node_btn = st.button('ADD NODE', use_container_width=True)
        if add_node_btn:
            new_node = NodeInDB(
                id = st.session_state.node_id,
                weights = json.dumps({'-1':''}),
                occupied = False,
                infos = json.dumps({'':''})
            )
            db.create_node([new_node])
