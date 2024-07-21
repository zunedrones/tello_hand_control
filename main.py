import cv2
from tello_zune import TelloZune
from hand_control import hand_gesture

tello = TelloZune()
tello.start_tello()

while True:
    frame = tello.get_frame()

    tello.calc_fps(frame)
    hand_gesture(tello, frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.end_tello()
cv2.destroyAllWindows()
