import cv2
import numpy as np
import time

class CaptureManager(object):

    def __init__(self, capture, previewWindowManager=None,
                 shouldMirrorPreview=False):

        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview


        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFliname = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._framesElapsed = int(0)
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(
                    channel=self.channel
                    )
            return self._frame

    @property
    def isWrittingImage(self):

        return self._imageFilename is not None

    @property
    def isWrittingVideo(self):

        return self._videoFliname is not None

    def enterFrame(self):
        """captura o proximo frame, se tiver"""

        assert not self._enteredFrame, \
            "frame entrou previamente e nao saiu"

        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        """desenha a canvas para captura"""

        if self.frame is None:
            self._enteredFrame = False
            return

        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed

        self._framesElapsed += 1

        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = np.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)

        if self.isWrittingImage:
            cv2.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None

        self._writeVideoFrame()

        self._frame = None
        self._enteredFrame = False

    def writeImage(self, filename):

        self._imageFilename = filename

    def startWritingVideo(
            self, filename,
            encoding=cv2.VideoWriter.fourcc('I', '4', '2', '0'),
            ):
        self._videoFliname = filename
        self._videoEncoding = encoding

    def stopWritingVideo(self):

        self._videoFliname = None
        self._videoEncoding = None
        self._videoWriter = None

    def _writeVideoFrame(self):

        if not self.isWrittingVideo:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                if self._framesElapsed < 20:
                    return
                else:
                    fps = self._fpsEstimate

            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

            self._videoWriter = cv2.VideoWriter(
                    self._videoFliname, self._videoEncoding,
                    fps, size)

            self._videoWriter.write(self._frame)








        
