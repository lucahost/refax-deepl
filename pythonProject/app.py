import PIL.Image

from moduls.config import predControlSize, appSize
from moduls.facedetection import cv2, detectFaces, faceBorders, addFaceBorders, getFaceImgInFirstBorder
from moduls.chartcontrols import radarChartImage
from moduls.mooddetection import classifyImage
from moduls.game import Game

# init video capture with appSize
cap = cv2.VideoCapture(0)
cap.set(3, appSize[0])
cap.set(4, appSize[1])

game = Game()
game.start()



def addImage(img, background,startpunkt=(0,0)):
    if img is None:
        return

    size = img.size if type(img) == PIL.Image.Image else img.shape[:2]

    x = startpunkt[0]
    y = startpunkt[1]
    background[y : size[1] + y, x:size[0] + x] = img
    return background

from PIL import Image as im
while True:
    success, img = cap.read()
    if not success:
        continue

    # add borders around detected faces
    faces = detectFaces(img)
    faceborders = faceBorders(faces)
    addFaceBorders(faceborders, img)

    # predict classes for detected face
    faceImg = getFaceImgInFirstBorder(faceborders, img)
    prediction = classifyImage(faceImg)

    # show predition control
    radar = radarChartImage(prediction)
    addImage(radar, img)

    # Game
    game.add_prediction(prediction)
    currentControl, globalControl = game.get_controls()
    controlsX = int(appSize[0] / 2 - game.global_score_control.control_size[0] / 2)
    controlHeight = game.global_score_control.control_size[1]

    addImage(currentControl, img,(controlsX , 40))
    addImage(globalControl, img, (controlsX , 40 + controlHeight))

    gameText = game.getInfoText()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,gameText,(controlsX,30),font,1,(0,0,255),2 )

    cv2.imshow('Input', img)
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
