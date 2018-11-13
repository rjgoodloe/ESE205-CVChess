import chess
import chess.uci
import numpy as np
from Board import Board

class ChessEng:

	def __init__(self, realBoard):

		self.engBoard = chess.Board()
		self.engine = chess.uci.popen_engine("/usr/games/stockfish")
		self.engine.uci()
		print(self.engBoard)

	def updateMove(self, move):

		uciMove = chess.Move.from_uci(move)
		if uciMove not in self.engBoard.legal_moves:
			print("Error: Invalid Move")
		else:
			self.engBoard.push(uciMove)
			#self.checkCircumstances()
			print(self.engBoard)


	def checkCircumstances(self):

		gameOver = False
		if self.engBoard.is_check() and not self.engBoard.is_checkmate():
			print("check")
		if self.engBoard.is_game_over():
			if self.engBoard.is_checkmate():
				print("Checkmate")
				gameOver = True
			elif self.engBoard.is_stalemate():
				print("Stalemate")
				gameOver = True

		return gameOver

	def feedToAI(self):


		self.engine.position(self.engBoard)
		response = self.engine.go(movetime=2000)
		bestMove = response[0]
		print("AI response:")
		print(bestMove)

		self.engBoard.push(bestMove)
		print(self.engBoard)
