# see https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
from Camera import Camera
from Image import Image
import cv2

camera=Camera()


while(True):
    # get and display an image
    image=camera.takePicture(800,800)
    Image.show("Preview",image)
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
camera.close()
cv2.destroyAllWindows()
