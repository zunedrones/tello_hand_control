import cv2
import tello_control
from tello_zune import TelloZune

tello = TelloZune()
tello.start_tello()

while True:
    # Obtem o frame da camera do drone
    frame = tello.get_frame()

    # Faz a detecção de gestos e movimenta o drone
    frame = tello_control.moves(tello, frame, simulate=False)
    
    # Escreve informações no frame
    tello.write_info(frame, fps=True, bat=True)
      
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.end_tello()
cv2.destroyAllWindows()
