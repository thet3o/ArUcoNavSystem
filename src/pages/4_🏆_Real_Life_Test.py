import streamlit as st
from aruco.aruco import detect_marker
import numpy as np
from streamlit_webrtc import webrtc_streamer
import streamlit as st
import cv2
import av
import glob

st.set_page_config(
    layout='centered'
)

video_file = open('../output_best.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)