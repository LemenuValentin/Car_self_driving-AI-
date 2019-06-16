import socketio
import eventlet
import base64
from PIL import Image
from io import BytesIO
import pandas as pd
import cv2
import numpy as np
import pickle

# Paramètres modifiables par le user pour déterminer les données à traîter
OS_Mac = 1
model_file_name_1 = "model_direction.pkl"
model_file_name_2 = "model_acceleration.pkl"

# Chargement du modèle
if OS_Mac == 1:
    path_model_1 = "/Users/anizetthomas/PycharmProjects/Car_self_driving/Linear_regression_model/" + model_file_name_1

else:   # Pour windows
    path_model_1 = "/Linear_regression_model/" + model_file_name_1

print(path_model_1)
model = pickle.load(open(path_model_1, 'rb'))

# create a Socket.IO server
sio = socketio.Server()

# event sent by the simulator
@sio.on('telemetry')
def telemetry(sid, data):

    if data:
        # The current steering angle of the car
        steering_angle = float(data["steering_angle"])
        # The current throttle of the car, how hard to push peddle
        throttle = float(data["throttle"])
        # The current speed of the car
        speed = float(data["speed"])


        # The current image from the center camera of the car
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        numpy_image = np.array(image)
        opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
        #attention l'image n'est pas en noir et blanc !

        median = cv2.medianBlur(opencv_image, 5)       # Floute l'image (5 paramètre floutage)
        edges = cv2.Canny(median, 100, 200)     # Trouver les grandes variations de couleur

        #cv2.imshow('edges',edges)
        #cv2.waitKey(0)

        index = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        Array_distanceleft = []
        Array_distanceright = []

        for n in index:
            pixels = np.argwhere(edges[n] == 255)  # Recherche le blanc (255) dans l'image
            if len(pixels[pixels < 160]) != 0:
                pixelsleft = pixels[pixels < 160]
                leftdetection = pixelsleft[len(pixelsleft) - 1]  # calcule la position moyenne de l'edge à gauche
                distanceleft = 160 - leftdetection
                Array_distanceleft.append(distanceleft)
            if len(pixels[pixels > 160]) != 0:
                pixelsright = pixels[pixels > 160]
                rightdetection = pixelsright[0]
                distanceright = rightdetection - 160
                Array_distanceright.append(distanceright)

        #if len(Array_distanceright) != 0 and len(Array_distanceleft) != 0:
            #print(max(Array_distanceleft) - min(Array_distanceleft))
        print(Array_distanceleft)
        print(len(Array_distanceleft))
        print(Array_distanceright)
        print(len(Array_distanceright))

        if (len(Array_distanceleft)) != 0:
            DistanceToLeft = np.median(Array_distanceleft)
        else:
            DistanceToLeft = 1000
        #print('Distance gauche = ',DistanceToLeft)

        if (len(Array_distanceright)) != 0:
            DistanceToRight = np.median(Array_distanceright)
        else:
            DistanceToRight = 1000
        #print('Distance gauche = ', DistanceToLeft)
        #print('Distance droite = ', DistanceToRight)

        if (len(Array_distanceleft)) != 0 and (len(Array_distanceright)) != 0:
            if (min(Array_distanceleft) < 50 and min(Array_distanceright) < 50):
                print('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
                index2 = [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85]
                Array_distanceleft2 = []
                Array_distanceright2 = []
                for n in index2:
                    pixels2 = np.argwhere(edges[n] == 255)  # Recherche les pixels blanc (255) dans l'image
                    if len(pixels2[pixels2 < 160]) != 0:
                        pixelsleft2 = pixels2[pixels2 < 160]
                        leftdetection2 = pixelsleft2[len(pixelsleft2) - 1]  # calcule la position moyenne de l'edge
                        distanceleft2 = 160 - leftdetection2  # distance  jusqu'au bord gauche de la route
                        Array_distanceleft2.append(distanceleft2)
                    if len(pixels2[pixels2 > 160]) != 0:
                        pixelsright2 = pixels2[pixels2 > 160]
                        rightdetection2 = pixelsright2[0]  # calcule la position moyenne de l'edge à droite !!
                        # Problème, si on sort un peu trop de la route, le premier à droite est la ligne gauche
                        distanceright2 = rightdetection2 - 160  # distance jusqu'au bord droit de la voiture
                        Array_distanceright2.append(distanceright2)
                if len(Array_distanceleft2) != 0:
                    #print("Array_left2",Array_distanceleft2)
                    DistanceToLeft = np.median(Array_distanceleft2)
                else:
                    DistanceToLeft = 1000
                if len(Array_distanceright2) != 0 :
                    #print("Array_right2", Array_distanceright2)
                    DistanceToRight = np.median(Array_distanceright2)
                else:
                    DistanceToRight = 1000
            else:
                DistanceToLeft = np.median(Array_distanceleft)
                DistanceToRight = np.median(Array_distanceright)

        #print('ArrayLeft', Array_distanceright)
        #print('DLeft',DistanceToLeft)
        #print('ArrayRight', Array_distanceright)
        #print('DRight',DistanceToRight)

        # Use your model to compute steering and throttle
        steer = model.predict(np.array([DistanceToLeft, DistanceToRight, throttle]).reshape(1,-1))
        steer = steer[0]
        #print(steer)
        #steer = 0              # Direction
        throttle = 0.5                      # Accélération
        speed = 1                           # Speed
        print(steer)
        #print(DistanceToLeft)
        #print(DistanceToRight)
        # response to the simulator with a steer angle and throttle
        send(steer, throttle)
    else:
        # Edge case
        sio.emit('manual', data={}, skip_sid=True)

# event fired when simulator connect
@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send(0, 0)

# to send steer angle and throttle to the simulator
def send(steer, throttle):
    sio.emit("steer", data={'steering_angle': str(steer), 'throttle': str(throttle)}, skip_sid=True)


# wrap with a WSGI application
app = socketio.WSGIApp(sio)

# simulator will connect to localhost:4567
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)