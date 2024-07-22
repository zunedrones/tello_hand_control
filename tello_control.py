import cv2
from hand_control import hand_gesture
from tracking_base import tracking
import time

hand_gesture_info = []
rect_detect = [0, 0, 0, 0]

def moves(tello, frame):
    hand_gesture_info = hand_gesture(frame)
    frame = hand_gesture_info[0]
    rect_detect = hand_gesture_info[1][0]
    actual_hand = hand_gesture_info[1][1]
    hand_classification = hand_gesture_info[1][2]

    print(hand_gesture_info[1])
    old_move = ''
    if hand_classification == 'Takeoff' and hand_classification != old_move:
        tello.send_cmd('takeoff')
        old_move = 'Takeoff'
        print("dei takeoff")
        time.sleep(1)
    elif hand_classification == 'Land' and hand_classification != old_move:
        tello.send_cmd('land')
        old_move = 'Land'
        print("dei land")
        time.sleep(4)
    elif hand_classification == 'Tracking' and old_move != "Land":
        tracking(tello, rect_detect)
    elif hand_classification == 'None' or hand_classification == 'Stop':
        tello.send_rc_control(0, 0, 0, 0)
    
    return frame

