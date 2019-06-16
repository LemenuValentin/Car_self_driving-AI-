# coding: utf-8

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import mmap
import pandas as pd
from sklearn import linear_model
import seaborn as sns
import cv2
from sklearn.linear_model import LinearRegression
from sklearn import datasets
from sklearn import linear_model
import pickle
import os

# Paramètres modifiables par le user pour déterminer les données à traîter
Data_to_treat = "Data_2"
result_csv_file = "Result.csv"
OS_Mac = 1


# 1) Modification du fichier csv afin de pouvoir traîter les données
if OS_Mac == 1:
    path = "/Users/anizetthomas/PycharmProjects/Car_self_driving/Training_data/"
    full_path = path + Data_to_treat
    print(full_path)
    print(full_path + '/driving_log.csv')
else:   # Pour windows
    path = "/Training_data/"
    full_path = path + Data_to_treat + '/'

ToAdd = "image_center,image_left,image_right,direction,acceleration,brake,speed"
with open(full_path + '/driving_log.csv', 'r+') as file:
    read = file.read()
    #print(read[0])
    if read[0] == 'i':
        file.close()
    else:
        with open(full_path + '/driving_log.csv', "w+") as f:
                f.write(ToAdd + "\n" + read)
                f.close()
car_data_bis = pd.read_csv(full_path + '/driving_log.csv', delimiter=',')
length = len(car_data_bis) - 1


# 2) Définition des différentes données à traîter
image_center = car_data_bis['image_center']
image_left = car_data_bis['image_left']
image_right = car_data_bis['image_right']
direction = car_data_bis['direction']
acceleration = car_data_bis['acceleration']
brake = car_data_bis['brake']
speed = car_data_bis['speed']


# 3) Traitement des données --> features
index = [90,91,92,93,94,95,96,97,98,99,100]
Array_distanceleft = []
Array_distanceright = []
Result = length*['']
i=0
ToAddResult = "distance_left,distance_right,direction,acceleration"
print(full_path + '/' + result_csv_file)
with open(full_path + '/' + result_csv_file, "w+") as f:
    f.write(ToAddResult + "\n")
    while i < length :
        for n in index:
            path = image_center[i]
            image = cv2.imread(path,0)
            median = cv2.medianBlur(image, 5)                   # Floute l'image (5 paramètre floutage)
            edges = cv2.Canny(median, 100, 200)                 # Trouver les grandes variations de couleur
            pixels = np.argwhere(edges[n] == 255)               # Recherche le blanc (255) dans l'image
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

        if len(Array_distanceleft) != 0:
            DistanceToLeft = np.median(Array_distanceleft)
        else:
            #print('---------------no info left----------------------')  # si aucun edge a été détecté à gauche
            DistanceToLeft = 1000

        if len(Array_distanceright) != 0:
            DistanceToRight = np.median(Array_distanceright)
        else:
            #print('---------------no info right----------------------')  # si aucun edge a été détecté à droite
            DistanceToRight = 1000

        Array_distanceleft = []
        Array_distanceright = []


        one_distance_left = DistanceToLeft
        one_distance_right = DistanceToRight
        one_direction = direction[i]
        one_acceleration = acceleration[i]
        interim_result = str(one_distance_left) + ',' + str(one_distance_right) + ',' + str(one_direction) + ',' + str(one_acceleration)

        f.write(interim_result + "\n")

        print(str(i) + "/" + str(length - 1) + "  Process data's ...")
        i += 1

f.close()