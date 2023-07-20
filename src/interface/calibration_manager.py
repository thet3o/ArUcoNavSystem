"""Nodes Manager

This is a small interface to interact with the nodes storage(sqlite db)

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'


from streamlit_extras.switch_page_button import switch_page
    
fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_READ)
mtx = fs.getNode('camera_matrix').mat()
dist = fs.getNode('dist_coeffs').mat()
fs.release()
def cam_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    out, _ = detect_marker(img, mtx, dist)
    return av.VideoFrame.from_ndarray(out, format="bgr24")
st.title('Calibrator')
colleft, colright = st.columns(2)
capture_btn = colleft.button('Capture Image')
cam = webrtc_streamer(key="live_webcam", video_frame_callback=cam_callback,)