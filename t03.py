import chardet
import os

path = os.getenv("HOME")+"/shape_predictor_68_face_landmarks.dat"

with open(path,"rb") as f1:
    file=f1.read()

