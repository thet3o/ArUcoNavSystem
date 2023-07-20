"""Enrty Point for interface

This is a small interface to interact with the nodes storage(sqlite db)

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import streamlit as st

st.set_page_config(
    page_title='Interface',
)

st.title('ArUcoNavSystem Interface')
st.write("Benvenuto questa è l'interfaccia di test del sistema di navigazione")

st.sidebar.warning('Seleziona un modulo')
    
