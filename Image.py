# part of https://github.com/rjgoodloe/ESE205-CVChess
import cv2
# Image handling - especially show for debug
class Image:
  @staticmethod
  def show(title,image):
      cv2.imshow(title,image)
      # dummy wait for a key for 1 millisecond
      cv2.waitKey(1)
