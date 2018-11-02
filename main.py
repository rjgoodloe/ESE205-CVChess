import cv2
import argparse
from board_Recognition import board_Recognition
from image_Analysis import image_Prep


# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#                help="path to the input image")
#ap.add_argument("-i", "--image2", required=True,
#                help="path to the input image")

#args =vars(ap.parse_args())

#image = cv2.imread(args["image"])
#image2 = cv2.imread(args["image2"])
image = cv2.imread('image1.jpg')
image2 = cv2.imread('image2.jpg')
	# Clean Image
#Image_Analyzer = image_Prep(image)
#cleanImage = Image_Analyzer.prepare_Image(image)


	# Recognize Board
boardRec = board_Recognition(image, image2)
boardRec.initialize_Board(image,image2)

	#on start
	#	take image
	#	clean image
	#	makeboard
	#		find edges
	#		makes squares
	#		assign squares to matrix
	#	IF NO MOVES MADE YET
	#	prompt ready for first move return to start
	#	ELSE
	#		image difference
	#			determine which squares leaving entering
	#			set current image to previous for next iteration
	#		feed image difference to chess engine
	#		display results in GUI
	#	on click return to start

