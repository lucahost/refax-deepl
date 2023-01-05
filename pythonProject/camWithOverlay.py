import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing import image


# face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# place of image
appSize = (1280, 720)
imgSize = (100, 100)
imgBorder = 10

imgPlace = (imgBorder,
            imgSize[0] + imgBorder,
            appSize[0] - imgSize[1] - imgBorder,
            appSize[0] - imgBorder)

# load happy/angry img & resize
angry = cv2.imread('Gnome-face-angry.png')
angry = cv2.resize(angry, imgSize)
happy = cv2.imread('happy.jpg')
happy = cv2.resize(happy, imgSize)

cap = cv2.VideoCapture(0)
cap.set(3, appSize[0])
cap.set(4, appSize[1])

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

count = 0
overlay = happy

def toggleImg(treshold):
    global count, overlay
    count += 1
    if count < treshold:
        return overlay
    count = 0
    overlay = angry if (overlay == happy).all() else happy


img_height = 224
img_width = 224
myModel = load_model('models/bigfoot-ubuntu.h5')
class_names = ['Neutral', 'Happy', 'Sad', 'Surprise', 'Fear', 'Disgust', 'Anger', 'Contempt']


def classifyImage(img):
    img = cv2.resize(img, (img_height, img_width))
    x = image.image_utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    prediction = myModel.predict(x)
    predlabel = class_names[prediction.argmax()]

    return predlabel


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    succes, img = cap.read()

    faces = face_cascade.detectMultiScale(img, 1.05, 4)
    if (len(faces) == 0):
        continue

    (x, y, w, h) = faces[0]

    print(faces[0])
    h = int(w * 1.3)
    y = int(y - (h - w) / 2)

    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    face = img[y:(y + h), x:(x + w)]
    img[0:h, 0:w] = face

    recClass = classifyImage(face)
    cv2.putText(img, recClass,
                org=(0, appSize[1]),
                fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                fontScale=3,
                color=(0, 255, 0),
                thickness=3)

    # img[imgPlace[0]:imgPlace[1], imgPlace[2]:imgPlace[3]] = overlay

    cv2.imshow('Input', img)

    # break if esc key pressed
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
