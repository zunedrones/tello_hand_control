import cv2
import mediapipe as mp
import time

FONT = cv2.FONT_HERSHEY_SIMPLEX
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_WHITE = (255, 255, 255)
ORG = (500, 30)
FONTSCALE = 1
THICKNESS = 2
VELOCITY = 20

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

def hand_gesture(tello, frame):

    # Convertendo a imagem para RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processando a imagem
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]

        # Desenhando as landmarks
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Acessando as landmarks 
        for id, lm in enumerate(hand_landmarks.landmark):
            h, w, _ = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)

            if id == 4:  # Ponta do polegar
                thumb_tip_y = lm.y
                thumb_tip_x = lm.x
            elif id == 8:  # Ponta do dedo indicador
                index_tip_y = lm.y
            elif id == 12:  # Ponta do dedo médio
                middle_tip_y = lm.y
            elif id == 16:  # Ponta do dedo anelar
                ring_tip_y = lm.y
            elif id == 20:  # Ponta do dedo mínimo
                pinky_tip_y = lm.y
                pinky_tip_x = lm.x
            elif id == 3:  # Junta do polegar
                thumb_mcp_y = lm.y
                thumb_mcp_x = lm.x
            elif id == 6:  # Junta do dedo indicador
                index_mcp_y = lm.y
            elif id == 10:  # Junta do dedo médio
                middle_mcp_y = lm.y
            elif id == 14:  # Junta do dedo anelar
                ring_mcp_y = lm.y
            elif id == 18:  # Junta do dedo mínimo
                pinky_mcp_y = lm.y
        
        # Gestos
        raised_thumb = (pinky_tip_x < thumb_tip_x and thumb_tip_x > thumb_mcp_x) or (pinky_tip_x > thumb_tip_x and thumb_tip_x < thumb_mcp_x)
        open_hand = raised_thumb and index_tip_y < index_mcp_y and middle_tip_y < middle_mcp_y and ring_tip_y < ring_mcp_y and pinky_tip_y < pinky_mcp_y
        closed_hand = not raised_thumb and index_tip_y > index_mcp_y and middle_tip_y > middle_mcp_y and ring_tip_y > ring_mcp_y and pinky_tip_y > pinky_mcp_y
        l_hand = raised_thumb and index_tip_y < index_mcp_y and middle_tip_y > middle_mcp_y and ring_tip_y > ring_mcp_y and pinky_tip_y > pinky_mcp_y
        two_hand = index_tip_y < index_mcp_y and middle_tip_y < middle_mcp_y and ring_tip_y > ring_mcp_y and pinky_tip_y > pinky_mcp_y
        four_hand = not raised_thumb and index_tip_y < index_mcp_y and middle_tip_y < middle_mcp_y and ring_tip_y < ring_mcp_y and pinky_tip_y < pinky_mcp_y

        # mao aberta
        if open_hand:
            cv2.putText(frame, 'FRONT', ORG, FONT, FONTSCALE, COLOR_GREEN, THICKNESS)
            tello.send_rc_control(0, VELOCITY, 0, 0)
        # mao fechada
        elif closed_hand:
            cv2.putText(frame, 'STOP', ORG, FONT, FONTSCALE, COLOR_RED, THICKNESS)
            tello.send_rc_control(0, 0, 0, 0)
        # mao em L
        elif l_hand:
            cv2.putText(frame, 'LAND', ORG, FONT, FONTSCALE, COLOR_BLUE, THICKNESS)
            tello.send_cmd('land')
            time.sleep(4)
        # Dois dedos
        elif two_hand:
            cv2.putText(frame, 'TAKEOFF', ORG, FONT, FONTSCALE, COLOR_WHITE, THICKNESS)
            tello.send_cmd('takeoff')
            time.sleep(4)
        # Quatro dedos
        elif four_hand:
            cv2.putText(frame, 'BACK', ORG, FONT, FONTSCALE, COLOR_YELLOW, THICKNESS)
            tello.send_rc_control(0, -VELOCITY, 0, 0)

        tello.send_rc_control(0, 0, 0, 0)



