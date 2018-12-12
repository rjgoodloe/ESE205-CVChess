import chess
import chess.uci
import numpy as np
import stockfish
from Board import Board

class ChessEng:

	def __init__(self, realBoard):

		self.engBoard = chess.Board()
		self.engine = chess.uci.popen_engine("/usr/games/stockfish")
		self.engine.uci()
		#self.engine.setoption({'Skill Level' : 0})
		#print(self.engine.options)
		print(self.engBoard)

	def updateMove(self, move):

		uciMove = chess.Move.from_uci(move)
		if uciMove not in self.engBoard.legal_moves:
			return 1
		else:
			self.engBoard.push(uciMove)
			print(self.engBoard)
			return 0


	def feedToAI(self):


		self.engine.position(self.engBoard)
		response = self.engine.go(movetime=2000)
		bestMove = response[0]
		self.engBoard.push(bestMove)
		f = open("Game.txt", "a+")
		f.write(bestMove.uci()+ "\r\n")
		f.close()
		print(self.engBoard)
		return bestMove




#	def setdif(self, value)

#		if value == 1
#		self.engine.setoption Skill Level 0
#			print("Easy")
#			return self.engine
#		elif value == 2
#		self.engine.setoption Skill Level 5
#			print("Itermediate")
#			return self.engine
#		elif value == 3
#		self.engine.setoption Skill Level 10
#			print("Hard")
#			return self.engine
#		elif value == 4
#		self.engine.setoption Skill Level 15
#			print("Extreme")
#			return self.engine
#		elif value == 5
#		self.engine.setoption Skill Level 20
#			print("Master")
#			return self.engine
#		return self.engine.setoption Skill Level value



#	def difconv(self. text)
#
#		if text == "Easy"
#			return 1
#		elif text == "Intermediate"
#			return 2
#		elif text == "Hard"
#			return 3
#		elif text == "Extreme"
#			return 4
#		elif text == "Master"
#			return 5


