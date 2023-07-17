from navigation.navigation import Node, dijkstra
from simulator.simulator import build_graph, show_graph, show_moving_robot
from aruco.aruco import detect_marker
import cv2
import imageio


if __name__ == '__main__':
    nodes = {
        '0': Node('0', {'1': 1}),
        '1': Node('1', {'0': 1,'3': 2}),
        '3': Node('3', {'1': 2,'4': 5,'5': 1}),
        '4': Node('4', {'3': 5}),
        '5': Node('5', {'3': 1,'6': 2}),
        '6': Node('6', {'5': 2,'3': 8}),
    }
    #print(graphd.edges)
    graph = [v for k, v in nodes.items()]
    show_moving_robot(graph, ['A', 'B', 'C', 'E'])
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
                    path_steps -= 1
                    print(f'next step {path_steps}')
                    next_node = path[path_steps-1] if path_steps != 1 else  f'{path[path_steps-1]} destination'
                else:
                    current_node = 'Arrived'
                    next_node = ''
                    running = False
                    
                    
        cv2.putText(img, f'Current Node: ', (0, height-150), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0,0,0), 3)
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