import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
class FaceBorder:
    def __init__(self, face):
        (x, y, w, h) = face
        # h = h * 1.2
        self.start = (x, y)
        self.end = (x + w, y + h)
        self.color = (255, 0, 0)  # blue
        self.thickness = 2


def faceBorders(faces):
    return [FaceBorder(face) for face in faces]


def addFaceBorders(img):
    faces = detectFaces(img)
    face_borders = faceBorders(faces)
    for border in face_borders:
        cv2.rectangle(img, border.start, border.end, border.color, border.thickness)
    return face_borders


def detectFaces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

def getFaceImgInFirstBorder(faceborders, img):
    if len(faceborders) == 0:
        return

    face_border = faceborders[0]
    x = face_border.start[0]
    y = face_border.start[1]
    x2 = face_border.end[0]
    y2 = face_border.end[1]
    return img[y:y2, x:x2]