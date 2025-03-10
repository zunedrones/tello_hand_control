import numpy as np

WIDTH = 960
HEIGHT = 720
#coordenadas do centro
CENTERX = WIDTH // 2
CENTERY = HEIGHT // 2

#coeficiente proporcional (obtido testando)
#determina o quanto a velocidade deve mudar em resposta ao erro atual
KP = 0.2
#coeficiente derivativo (obtido testando)
#responsável por controlar a taxa de variação do erro
KD = 0.2

#erro anterior
prevErrorX = 0
prevErrorY = 0

def tracking(tello, rect):
    '''
    Faz o tracking do objeto detectado na imagem
    Args:
        tello (TelloZune): objeto do drone
        rect (list): lista com 4 valores [x1, y1, x2, y2] que representam as coordenadas do objeto
    
    Returns
        None
    '''
    global prevErrorX, prevErrorY
    x1, y1, x2, y2 = rect
    speedFB = 0
    # detectWidth = x2 - x1
    cxDetect = (x2 + x1) // 2
    cyDetect = (y2 + y1) // 2

    #PID - Speed Control
    area = (x2 - x1) * (y2 - y1)
    
    if (rect != [0, 0, 0, 0]):
        errorX = cxDetect - CENTERX
        errorY = CENTERY - cyDetect

        if area < 27000: 
            speedFB = 25
        elif area > 120000:
            speedFB = -25
            # print(f"AREA: {area}")
    else:
        errorX = 0
        errorY = 0
        print("0 DETECTIONS")
        # print(f"AREA: {area_land}")

    #velocidade de rotação em torno do próprio eixo é calculada em relação ao erro horizontal
    speedYaw = KP*errorX + KD*(errorX - prevErrorX)
    speedUD = KP*errorY + KD*(errorY - prevErrorY)
    #não permite que a velocidade 'vaze' o intervalo -100 / 100
    speedYaw = int(np.clip(speedYaw,-100,100))
    speedUD = int(np.clip(speedUD,-100,100))
    
    print(f"FB: {speedFB}, UD: {speedUD}, YAW: {-speedYaw}")
    if(rect != [0, 0, 0, 0]):
        tello.send_rc_control(0, speedFB, speedUD, -speedYaw)
    else:
        tello.send_rc_control(0, 0, 0, 0)
    #o erro atual vira o erro anterior
    prevErrorX = errorX
    prevErrorY = errorY