import cv2


def draw_bounding_box(img, top_left, top_right, bottom_left, bottom_right):
    cv2.line(img, top_left, top_right, (0, 255, 0), 2)
    cv2.line(img, top_right, bottom_right, (0, 255, 0), 2)
    cv2.line(img, bottom_right, bottom_left, (0, 255, 0), 2)
    cv2.line(img, bottom_left, top_left, (0, 255, 0), 2)
    return img

def draw_center(img, top_left, bottom_right):
    cx = int((top_left[0] + bottom_right[0]) / 2.0)
    cy = int((top_left[1] + bottom_right[1]) / 2.0)
    cv2.circle(img, (cx, cy), 4, (0, 0, 255), -1)
    return img
    
def draw_marker_data(img, top_left, data):
    cv2.putText(img, str(data), (top_left[0], top_left[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    return img