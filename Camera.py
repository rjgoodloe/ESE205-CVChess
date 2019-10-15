# part of https://github.com/rjgoodloe/ESE205-CVChess
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera, PiCameraError
import time
import cv2
import imutils

# camera access
class Camera:

  # construct me
  def __init__(self):
    # need to check whetheer PiCamera is available
    # https://www.raspberrypi.org/forums/viewtopic.php?t=46113
    try:
      self.picam = PiCamera()
      self.cam=picam
      self.webcam=None
    except PiCameraError as e:
      self.picam=None
      self.webcam = cv2.VideoCapture(0)
      self.cam=self.webcam
      if not self.webcam:
        print ("Camera failure: %s" % (str(e)))

  # take a picture
  def takePicture(self):
    if self.picam:
      return self.takePictureFromPiCam()
    elif self.webcam:
      return self.webcam.read()
    else:
      raise Exception('no camera available')
      

  def takePictureFromPiCam(self):
    # initialize the camera and grab a reference to the raw camera capture
    rawCapture = PiRGBArray(self.picam)

    # allow the camera to warmup
    time.sleep(1)

    # grab an image from the camera
    self.cam.capture(rawCapture, format="bgr")
    image = rawCapture.array
    resized = imutils.resize(image, height = 400, width = 400)


    return resized
