# see https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
from Camera import Camera
import cv2
import imutils

camera=Camera()
startImage=camera.takePicture()

while(True):
    # get and display an image
    image=camera.takePicture()
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diffImage=cv2.absdiff(image,startImage)
    cv2.imshow("Diff",diffImage)
    # https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    gray = cv2.cvtColor(diffImage, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cv2.imshow("Thresh",thresh)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours
    for c in cnts:
      # compute the bounding box of the contour and then draw the
      # bounding box on both input images to represent where the two
      # images differ
      (x, y, w, h) = cv2.boundingRect(c)
      cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow("Image",image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
camera.close()
cv2.destroyAllWindows()
