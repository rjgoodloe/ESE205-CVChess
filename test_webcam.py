import cv2

# see https://subscription.packtpub.com/book/hardware_and_creative/9781785285066/7/ch07lvl1sec41/working-with-webcam-using-opencv
# test the web camera 
def test_WebCamera():
  # initialize the camera
  cam = cv2.VideoCapture(0)
  ret, image = cam.read()

  if ret:
    cv2.imshow('SnapshotTest',image)
    #cv2.waitKey(0)
    cv2.destroyWindow('SnapshotTest')
    cv2.imwrite('/tmp/SnapshotTest.jpg',image)
  cam.release()

# call the camera test 
test_WebCamera()
