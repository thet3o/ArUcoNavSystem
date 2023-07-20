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
st.title('Test Live')
fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_READ)
mtx = fs.getNode('camera_matrix').mat()
dist = fs.getNode('dist_coeffs').mat()
fs.release()


def video_callback(frame):
    img = frame.to_ndarray(format='bgr24')
    out, _ = detect_marker(img, mtx, dist)
    
    return av.VideoFrame.from_ndarray(out, format="bgr24")

webrtc_streamer(key='cam', video_frame_callback=video_callback, video_receiver_size=100)
