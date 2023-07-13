from navigation.navigation import Node, dijkstra
from simulator.simulator import build_graph, show_graph, show_moving_robot
from aruco.aruco import detect_marker
import cv2
import time


if __name__ == '__main__':
    nodes = {
        '0': Node('0', {'1': 1}),
        '1': Node('1', {'0': 1,'2': 2}),
        '2': Node('2', {'1': 2,'4': 5,'5': 1,'3': 6}),
        '3': Node('3', {'2': 6,'6': 8}),
        '4': Node('4', {'2': 5}),
        '5': Node('5', {'2': 1,'6': 2}),
        '6': Node('6', {'5': 2,'3': 8}),
    }
    #print(graphd.edges)
    graph = [v for k, v in nodes.items()]
    #show_graph(graphd)
    show_moving_robot(graph, ['A', 'B', 'C', 'E'])
    path = dijkstra(nodes, '0', '5')
    print(path)
    graphd, edge_colors = build_graph(nodes, path)
    #show_graph(graphd, edge_colors)
    
    fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_READ)
    mtx = fs.getNode('camera_matrix').mat()
    dist = fs.getNode('dist_coeffs').mat()
    fs.release()
    
    cap = cv2.VideoCapture(1)
    
    path_steps = len(path)
    path.reverse()
    
    print(path)
    print(path[path_steps-1])
    
    running = True
    
    while running:
        ret, img = cap.read()
        #img = cv2.imread('/Users/thet3o/Pictures/b.jpg')
        h, w, _ = img.shape
        
        img, marker_list = detect_marker(img, w, mtx, dist)
        if marker_list != []:
            print(marker_list)
        for marker in marker_list:
            if str(marker['id']) == path[path_steps-1]:
                if path_steps > 1:
                    print(f'Node {path[path_steps-1]} passed')
                    path_steps -= 1
                    print(path_steps)
                else:
                    print(f'Node {path[path_steps-1]}, arrived to destination')
                    running = False
        cv2.imshow('debug', img)

            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()