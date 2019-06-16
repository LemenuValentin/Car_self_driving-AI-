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
from sklearn.metrics import r2_score
import pickle

# Paramètres modifiables par le user pour déterminer les données à traîter
Data_to_treat = "Data_2"
result_csv_file = "Result.csv"
model_file_name_1 = "model_direction.pkl"
model_file_name_2 = "model_acceleration.pkl"
OS_Mac = 1


# 1) Chargement des données d'apprentissage
if OS_Mac == 1:
    path = "/Users/anizetthomas/PycharmProjects/Car_self_driving/Training_data/"
    full_path = path + Data_to_treat + '/' + result_csv_file
    path_model_1 = "/Users/anizetthomas/PycharmProjects/Car_self_driving/Linear_regression_model/" + model_file_name_1
    path_model_2 = "/Users/anizetthomas/PycharmProjects/Car_self_driving/Linear_regression_model/" + model_file_name_2

else:   # Pour windows
    path = "Training_data/"
    full_path = path + Data_to_treat + '/' + result_csv_file
    path_model_1 = "/Linear_regression_model/" + model_file_name_1
    path_model_2 = "/Linear_regression_model/" + model_file_name_2

Result_data = pd.read_csv(full_path, delimiter=',')
length = len(Result_data)-1

distance_left     = Result_data['distance_left']
distance_right    = Result_data['distance_right']
direction         = Result_data['direction']
acceleration      = Result_data['acceleration']


# 2) Modèle de régression linéaire
label_1 = direction
label_2 = acceleration
features_test = Result_data.drop('direction', axis=1)

# Modèle de régression linéaire
regr_1 = linear_model.LinearRegression()
regr_1.fit(features_test,label_1)

regr_2 = linear_model.LinearRegression()
regr_2.fit(features_test,label_2)

#plt.scatter(acceleration, direction)
#plt.show()

pickle.dump(regr_1, open(path_model_1, "wb"))
model_1 = pickle.load(open(path_model_1, 'rb'))

pickle.dump(regr_2, open(path_model_2, "wb"))
model_2 = pickle.load(open(path_model_2, 'rb'))
