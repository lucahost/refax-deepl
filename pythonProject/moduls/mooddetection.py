from keras.models import load_model
from keras.preprocessing import image
import cv2
import numpy as np

from pythonProject.moduls.facedetection import getFaceImgInFirstBorder

myModel = load_model('models/bigfoot-ubuntu.h5')
img_height = 224
img_width = 224


def classify_face_in_first_border(face_borders, img):
    face_img = getFaceImgInFirstBorder(face_borders, img)
    return classify_image(face_img)

def classify_image(img):
    if img is None:
        return
    if img.size == 0:
        return

    img = cv2.resize(img, (img_height, img_width))
    x = image.image_utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    prediction = myModel.predict(x)
    return prediction[0]
