from hand_control import hand_gesture
from tracking import tracking
import time

hand_gesture_info = []
rect_detect = [0, 0, 0, 0]

def moves(tello, frame, simulate: bool = True):
    """
    Função que detecta os gestos e movimenta o drone
    Args:
        tello (TelloZune): Objeto do drone
        frame (np.array): Frame da camera do drone
        simulate (bool): Não faz com que o drone se movimente, apenas simula. Default: True
    Returns:
        frame (np.array): Frame da camera do drone
    """
    # Obtem a informação e faz a detecção de gestos
    hand_gesture_info = hand_gesture(frame)
    # Desenha no frame
    frame = hand_gesture_info[0]
    # Obtém o bounding box da mão
    rect_detect = hand_gesture_info[1][0]
    # Obtém qual foi o gesto feito
    hand_classification = hand_gesture_info[1][2]

    old_move = ''
    if not simulate:
        if hand_classification == 'Takeoff' and hand_classification != old_move:
            # Realiza o takeoff se o sinal for um V
            tello.takeoff()

            old_move = 'Takeoff'
            print("dei takeoff")

            time.sleep(1)
        elif hand_classification == 'Land':
            # Realiza o land se o sinal for um L
            tello.land()

            old_move = 'Land'
            print("dei land")

            time.sleep(1)
        elif hand_classification == 'Tracking' and old_move != "Land":
            # Realiza o tracking se o sinal for uma mão aberta
            tracking(tello, rect_detect)
        elif (hand_classification == 'None' or hand_classification == 'Stop') and old_move != 'Land':
            # Para o drone se o sinal for uma mão fechada
            tello.send_rc_control(0, 0, 0, 0)

            print("PAREI")
    
    return frame

