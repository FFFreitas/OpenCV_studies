import cv2

clicked = False


def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.cv.EVENT_LBUTTONUP:
        clicked = True


cameraCapture = cv2.VideoCapture(0)
cv2.namedWindow("Janela")
cv2.setMouseCallback("Janela", onMouse)

print("Mostrando o feed da camera. Click na janela ou aperte qualquer tecla")
success, frame = cameraCapture.read()
while success and cv2.waitKey(1) == -1 and not clicked:
    cv2.imshow("Janela", frame)
    success, frame = cameraCapture.read()

cv2.destroyWindow("Janela")
