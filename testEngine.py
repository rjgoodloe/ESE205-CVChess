import chess
from ChessEng import ChessEng

class testEngine:

	def __init__(self):

		Engine = ChessEng(0)
		gameOver = False
		while not gameOver:
			Engine.feedToAI()
			gameOver = Engine.checkCircumstances()


