# tello_hand_control
A Tello drone controled by hand gestures, using opencv, mediapipe and tensorflow.

![image](https://github.com/user-attachments/assets/6d240273-a62f-492a-b1c9-ec88090aa683)


The hand gesture detection model is built upon [another project](https://github.com/kinivi/hand-gesture-recognition-mediapipe/tree/main) that utilizes hand landmarks obtained through Mediapipe to train the model.

# Requeriments

* Python >= 3.9.0
  
```bash
pip install mediapipe
```
```bash
pip install opencv-python
```
```bash
pip install tensorflow
```
# Run the project

```bash
git clone https://github.com/zunedrones/tello_hand_control.git
cd tello_hand_control
python main.py
```
* You need to be connected to the Tello's Wi-Fi network to run the program.


