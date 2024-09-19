import cv2
import tello_control
from tello_zune import TelloZune

tello = TelloZune()
tello.start_tello()

while True:
    frame = tello.get_frame()

    frame = tello_control.moves(tello, frame)
    tello.calc_fps(frame)
      
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    """ if cv2.waitKey(1) & 0xFF == ord('t'):
        tello.send_cmd('takeoff')
        print('dei takeoff') """

tello.end_tello()
cv2.destroyAllWindows()
