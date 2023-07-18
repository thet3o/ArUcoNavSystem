"""Main

This is the main script of the entire program where everything starts here

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

from navigation.navigation import Node, dijkstra
from simulator.simulator import build_graph, show_graph
from aruco.aruco import detect_marker
import cv2
import imageio
from data.database import Database
import time

INSERT_DB = False


if __name__ == '__main__':
    db = Database('sqlite:///database.sqlite')
        
    nodes = db.get_nodes()
    
    print(nodes)
        
    graph = [v for k, v in nodes.items()]
    path = dijkstra(nodes, '0', '4')
    print(path)
    graphd, edge_colors = build_graph(nodes, path)
    #show_graph(graphd, edge_colors)
    
    fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_READ)
    mtx = fs.getNode('camera_matrix').mat()
    dist = fs.getNode('dist_coeffs').mat()
    fs.release()
    
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("test.mp4")
    
    path_steps = len(path)
    path.reverse()
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    wrt = imageio.get_writer("../output.mp4", fps=25)
    
    previous_marker_id = ''
    
    current_node = ''
    next_node = path[-1]
    running = True
    
    for k,v in nodes.items():
        db.update_node(k, occupied=False)

    while True:
        ret, img = cap.read()
        
        if not ret:
            break

        img, marker_list = detect_marker(img, mtx, dist)
        for marker in marker_list:
            if marker['id'] != previous_marker_id:
                print(f'Marker {marker["id"]}')
                previous_marker_id = marker['id']
            if str(marker['id']) == path[path_steps-1]:
                if path_steps > 1:
                    current_node = path[path_steps-1]
                    if path_steps < len(path):
                        db.update_node(path[path_steps], occupied=False)
                    db.update_node(current_node, occupied=True)
                    path_steps -= 1
                    print(f'next step {path_steps}')
                    next_node = path[path_steps-1] if path_steps != 1 else  f'{path[path_steps-1]} destination'
                else:
                    db.update_node(current_node, occupied=True)
                    time.sleep(0.5)
                    current_node = 'Arrived'
                    next_node = ''
                    running = False
                    
                    
        cv2.putText(img, 'Current Node: ', (0, height-150), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0,0,0), 3)
        cv2.putText(img, current_node, (300, height-150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 3)
        cv2.putText(img, 'Next node in path: ', (0, height-100), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 3)
        
        for i in reversed(range(len(path))):
            cv2.putText(img, f'{path[i]} ', (int((width/len(path))*i), height-40), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0) if i != path_steps-1 else (255, 255, 0), 3)
        
        wrt.append_data(img)
        cv2.imshow('debug', img)
        
        if not running:
            break
        
            
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        
    wrt.close()
    cap.release()
    cv2.destroyAllWindows()