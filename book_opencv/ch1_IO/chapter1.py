import cv2
import numpy as np
import os


# We can change the format extension from one to another
image = cv2.imread('file_14161_GabenKingdom.jpg')
cv2.imwrite('Glorious_Gaben.png', image)

# By default imread() returns an BGR (blue-red-green) image, even if the file is gray-scale
# we can especify the mode to be loaded, e.g: lets load the gabenewell image as gray-sacle image:

graygaben = cv2.imread('Glorious_Gaben.png', cv2.IMREAD_GRAYSCALE)
cv2.imwrite('GrayScale_Gaben.png', graygaben)

# Converting between an image and raw bytes
# OpenCV "sees" an image as 2D (usually gray-scale) or 3D numpy.array. An 8-bit
# gray-scalr image is a 2D contains bit values. A 24-bit RGB image is a 3D array
# we can access the values by using their respective index

bgrArray = bytearray(image)
grayArray = bytearray(graygaben)

# converting into arrays
grayImage = np.array(grayArray)
bgrImage = np.array(bgrArray)

# check size
grayImage.shape
bgrImage.shape

# resizing it for a 2D and 3D images
grayImage = grayImage.reshape(640, 360)
bgrImage = bgrImage.reshape(640, 360, 3)

grayImage.shape
bgrImage.shape

# we can also create a random image
randomByteArray = bytearray(os.urandom(120000))

flatnumpyarray = np.array(randomByteArray)

# convert it to 2D (400 x 300) grayscale image

randomGrayImage = flatnumpyarray.reshape(300, 400)
cv2.imwrite('RandomGray.png', randomGrayImage)

# Reading/Writing a video file
# OpenCV provides the VideoCapture and VideoWriter classes that support various
# video file formats. The supported formats vary by system but should always 
# include AVI. Via its read() method, a VideoCapture class may be polled 
# for new frames until reaching the end of its video file

RollCapture = cv2.VideoCapture('/home_2/Datasets/Rick Astley - Never Gonna Give You Up (Official Music Video).mp4')
fps = RollCapture.get(cv2.CAP_PROP_FPS)
size = (int(RollCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(RollCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
videoWriter = cv2.VideoWriter(
        '/home_2/Datasets/He_will_never_let_you_down.avi',
        cv2.VideoWriter.fourcc('I', '4', '2', '0'),
        fps,
        size
        )
succes, frame = RollCapture.read()
while succes:
    videoWriter.write(frame)
    succes, frame = RollCapture.read()

# Capturing camera frames
# A stream of camera frames is represented by the VideoCapture class, too.
# However, for a camera, we construct a VideoCapture class by passing the
# camera's device index instead of a video's filename. Let's consider an example
# that captures 10 seconds of video from a camera and writes it to an AVI file:

cameraCapture = cv2.VideoCapture(0)
fps = 30  # lame
size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

videoWriter = cv2.VideoWriter(
        'muito_gato.avi',
        cv2.VideoWriter.fourcc('I', '4', '2', '0'),
        fps,
        size
        )
succes, frame = cameraCapture.read()
numFramesRemaining = 10 * fps - 1
while succes and numFramesRemaining > 0:
    videoWriter.write(frame)
    succes, frame = cameraCapture.read()
    numFramesRemaining -= 1


cameraCapture.release()
