from keras.models import load_model
from keras.preprocessing import image
import cv2
import numpy as np


myModel = load_model('models/bigfoot-ubuntu.h5')
img_height = 224
img_width = 224
def classifyImage(img):
    if img is None:
        return
    if img.size == 0:
        return

    img = cv2.resize(img, (img_height, img_width))
    x = image.image_utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    prediction = myModel.predict(x)
    return prediction[0]

