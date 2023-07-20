import streamlit as st
from aruco.aruco import detect_marker
import numpy as np
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
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

class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format='bgr24')
        out, _ = detect_marker(img, mtx, dist)
    
        return av.VideoFrame.from_ndarray(out, format="bgr24")

#def video_callback(frame):
#    img = frame.to_ndarray(format='bgr24')
#    out, _ = detect_marker(img, mtx, dist)
#    
#    return av.VideoFrame.from_ndarray(out, format="bgr24")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


webrtc_streamer(key='cam', video_processor_factory=VideoProcessor, rtc_configuration=RTC_CONFIGURATION,
                async_processing=True, media_stream_constraints={"video": True, "audio": False},)
