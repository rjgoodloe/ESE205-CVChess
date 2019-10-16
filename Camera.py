# part of https://github.com/rjgoodloe/ESE205-CVChess
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera, PiCameraError
import time
import cv2
import imutils

# camera access
class Camera:
  debug=False

  # construct me
  def __init__(self):
    self.webcam=None
    # need to check whetheer PiCamera is available
    # https://www.raspberrypi.org/forums/viewtopic.php?t=46113
    try:
      self.picam = PiCamera()
      self.cam=picam
    except PiCameraError as e:
      self.picam=None
      self.getWebCam()
      if not self.webcam:
        print ("Camera failure: %s" % (str(e)))

  def getWebCam(self):
      if self.webcam is not None:
        # https://stackoverflow.com/a/44455417/1497139
        self.webcam.release()
      self.webcam=cv2.VideoCapture(0)
      self.cam=self.webcam
      return self.webcam

  # take a picture
  def takePicture(self,height=400,width=400):
    if self.picam:
      image=self.takePictureFromPiCam()
    elif self.webcam:
      self.getWebCam()
      ret,image=self.webcam.read()
      if not ret:
        raise Exception('webcam image read failed')
    else:
      raise Exception('no camera available')
    resized = imutils.resize(image.copy(), height = height, width = width)
    if Camera.debug:
      cv2.imshow('camera',image)
      cv2.imshow('resized',resized)
    return resized 

  def takePictureFromPiCam(self):
    # initialize the camera and grab a reference to the raw camera capture
    rawCapture = PiRGBArray(self.picam)

    # allow the camera to warmup
    time.sleep(1)

    # grab an image from the camera
    self.cam.capture(rawCapture, format="bgr")
    image = rawCapture.array
    return resized

  def close(self):
    if self.webcam:
      self.webcam.release()
