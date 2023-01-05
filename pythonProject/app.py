from moduls.chartcontrols import radar_chart_image
from moduls.config import app_config as config
from moduls.facedetection import cv2, addFaceBorders
from moduls.game.control import add_image
from moduls.game.game import Game
from moduls.handdetection import FindHands
from moduls.mooddetection import classify_face_in_first_border

# init video capture with appSize
cap = cv2.VideoCapture(0)
cap.set(3, config.app_size[0])
cap.set(4, config.app_size[1])

detector = FindHands.FindHands()

game = Game()

while True:
    success, img = cap.read()
    if not success:
        continue
    raw_img = cv2.flip(img, 1)
    overlay_radar = raw_img.copy()
    overlay_game = raw_img.copy()

    # detect touch of game_control
    index_fingers = detector.get_index_fingers(overlay_game)
    game.start_if_touched(index_fingers)

    # add borders around detected faces
    face_borders = addFaceBorders(overlay_radar)

    # predict classes for detected face
    prediction = classify_face_in_first_border(face_borders, raw_img)

    # show prediction control
    radar_control = radar_chart_image(prediction)
    add_image(radar_control, overlay_radar)

    # Game
    game.add_prediction(prediction)
    game_control = game.get_control()
    add_image(game_control, overlay_game)

    alpha = 1
    cv2.addWeighted(overlay_game, alpha, raw_img, 1 - alpha, 0, raw_img)

    alpha = 0.7
    cv2.addWeighted(overlay_radar, alpha, raw_img, 1 - alpha, 0, raw_img)

    cv2.imshow('Input', raw_img)
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
