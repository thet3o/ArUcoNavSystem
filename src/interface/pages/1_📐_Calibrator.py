from calibration.calibration import read_charuco, calibrate_camera
from aruco.aruco import detect_marker
import numpy as np
from streamlit_webrtc import webrtc_streamer
import streamlit as st
import cv2
import av
import glob
from streamlit_extras.metric_cards import style_metric_cards
import copy
st.title('Calibrator')

mcol1, mcol2 = st.columns(2, gap='large')

if 'calibration_images' not in st.session_state:
    st.session_state['calibration_images'] = []

mcol1.subheader('Image Capturing')
cam = mcol1.camera_input('')



if cam is not None:
    st.session_state['calibration_images'].append(cam.getvalue())

with mcol1.container():
    col1, col2, col3 = mcol1.columns(3)
    save_img_btn = col1.button('Save2Disk')
    delete_imgs_btn = col2.button('Delete All')
    if delete_imgs_btn:
        del st.session_state['calibration_images']
        st.session_state['calibration_images'] = []
    if save_img_btn:
        count = 0
        for bytes in st.session_state['calibration_images']:
            img = cv2.imdecode(np.frombuffer(bytes, np.uint8), cv2.IMREAD_COLOR)
            cv2.imwrite(f'calibration_images/in/cal{count}.jpg', img)
            count += 1
    counter = col3.metric('Captures:', len(copy.deepcopy(st.session_state.calibration_images)))
    
    
mcol2.subheader('Calibration')
with mcol2.container():
    calibration_btn = mcol2.button('Calibrate')
    
    if calibration_btn:
        imgs = copy.deepcopy(st.session_state.calibration_images)
        if len(imgs) > 5:
            with st.spinner('Calibrating, wait a few seconds...'):
                images = []
                images_bytes = copy.deepcopy(st.session_state['calibration_images'])
                del st.session_state['calibration_images']
                for bytes in images_bytes:
                    img = cv2.imdecode(np.frombuffer(bytes, np.uint8), cv2.IMREAD_COLOR)
                    images.append(img)
                all_corners, all_ids, imsize = read_charuco(images)
                ret, mtx, dist, rvecs, tvecs = calibrate_camera(all_corners, all_ids, imsize)
                # Save calibration data
                fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_WRITE)
                fs.write('camera_matrix', mtx)
                fs.write('dist_coeffs', dist)
                fs.release()
            st.session_state['calibration_images'] = []
            st.success('Calibration completed!')
        else:
            st.warning('Take more photos')