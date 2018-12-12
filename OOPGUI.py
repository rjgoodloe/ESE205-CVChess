import tkinter as tk
from tkinter import *
from Game import Game

LARGE_FONT = ("system", 20)
MED_FONT = ("system", 12)
SMALL_FONT = ("system", 8)


class Application(tk.Tk):
	'''
	This class controls the Graphical User Interface
	'''
	def __init__(self,*args, **kwargs):

		tk.Tk.__init__(self,*args,**kwargs)
		container = tk.Frame(self)

		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0,weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}

		self.game = Game()

		# holds CPU move information to be displayed in CPUMovePage
		self.move = StringVar()
		self.move.set( "e2")
		# holds winner information to be displayed in GameOverPage
		self.winner = StringVar()
		self.winner.set("CPU Wins!")

		# Give page objects to Application to show frame
		for F in (StartGamePage, InitializeBoardPage,SetBoardPage, ChooseColorPage,
				ChooseDifficultyPage, CPUMovePage, PlayerMovePage, CheckPage,
				CPUMoveErrorPage, GameOverPage, PlayerMoveErrorPage, ChoosePromotionPage):

			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky = "nsew")

		self.show_frame(StartGamePage)


	def show_frame(self,cont):

		frame = self.frames[cont]
		frame.tkraise()

class StartGamePage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "ESE 205: Computer Vision Chess", font = LARGE_FONT)
		label.pack(pady = 20, padx = 20)

		startGameButton = tk.Button(self, text = "Start New Game",font = MED_FONT,
						command = lambda: [controller.show_frame(InitializeBoardPage), controller.game.setUp()])
		startGameButton.pack()


class InitializeBoardPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Clear Board for Game Set Up", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		initBoardButton = tk.Button(self, text = "Done",font = MED_FONT, command = lambda : [controller.show_frame(SetBoardPage), controller.game.analyzeBoard()])
		initBoardButton.pack()

class ChooseColorPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Which color would you like to play?", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		blackButton = tk.Button(self, text = "Red (Black)",font = MED_FONT,
					command = lambda : [controller.show_frame(CPUMovePage),controller.move.set(controller.game.CPUMove())])
		blackButton.pack()

		whiteButton = tk.Button(self, text = "Blue (White)",font = MED_FONT,
					command = lambda: controller.show_frame(PlayerMovePage))
		whiteButton.pack()

class SetBoardPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Game Initialization Done. Set Board", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		setBoardButton = tk.Button(self, text = "Done",font = MED_FONT,
						 command = lambda : [controller.show_frame(ChooseDifficultyPage),controller.game.checkBoardIsSet()])
		setBoardButton.pack()

class PlayerMovePage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Your Move", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		PlayerButton = tk.Button(self, text = "Done",font = MED_FONT,
						command = lambda : [controller.game.playerMove(),self.checkValid(controller)])
		ResignButton = tk.Button(self, text = "Resign",font = SMALL_FONT,
						command = lambda : controller.show_frame(GameOverPage))
		PlayerButton.pack()
		ResignButton.pack()

	def checkValid(self,controller):
		if controller.game.over:
			controller.winner.set(contoller.game.winner)
			controller.show_frame(GameOverPage)
		elif controller.game.board.promo:
			controller.show_frame(ChoosePromotionPage)
		elif controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)

class CPUMovePage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "CPU Move:", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		self.moveLabel = tk.Label(self, textvariable = controller.move, font = MED_FONT)
		self.moveLabel.pack(pady = 10, padx = 10)
		CPUButton = tk.Button(self, text = "Done",font = MED_FONT,
						command = lambda : [controller.game.updateCurrent(), self.checkValid(controller)])
		CPUButton.pack()

	def checkValid(self,controller):
		if controller.game.over:
			controller.winner.set(controller.game.winner)
			controller.show_frame(GameOverPage)
		elif controller.game.isCheck:
			controller.show_frame(CheckPage)
		elif controller.game.CPUMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(CPUMoveErrorPage)
		else:
			controller.show_frame(PlayerMovePage)

class CheckPage(tk.Frame):

        def __init__(self,parent,controller):

                tk.Frame.__init__(self,parent)
                label = tk.Label(self,text = "You are in Check", font = LARGE_FONT)
                label.pack(pady = 10, padx = 10)
                setBoardButton = tk.Button(self, text = "Proceed",font = MED_FONT,
                                                 command = lambda : controller.show_frame(PlayerMovePage))
                setBoardButton.pack()

class CPUMoveErrorPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "That was not the correct CPU move", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		setBoardButton = tk.Button(self, text = "Try Again",font = MED_FONT,
						command = lambda : controller.show_frame(CPUMovePage))
		setBoardButton.pack()


class PlayerMoveErrorPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Error Invalid Move", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		setBoardButton = tk.Button(self, text = "Try Again", font = MED_FONT,
						command = lambda : controller.show_frame(PlayerMovePage))
		setBoardButton.pack()

class GameOverPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Game Over", font = LARGE_FONT)
		self.winnerLabel = tk.Label(self, textvariable = controller.winner, font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		self.winnerLabel.pack(pady = 10, padx = 10)

class ChooseDifficultyPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Choose the difficulty")
		label.pack(pady = 10, padx = 10)

		EasyButton = tk.Button(self, text = "Easy",
						command = lambda : [self.setEasy(controller), controller.show_frame(ChooseColorPage)])
		EasyButton.pack()

		IntermediateButton = tk.Button(self, text = "Intermediate",
						command = lambda : [self.setIntermediate(controller), controller.show_frame(ChooseColorPage)])
		IntermediateButton.pack()

		HardButton = tk.Button(self, text = "Hard",
						command = lambda : [self.setHard(controller), controller.show_frame(ChooseColorPage)])
		HardButton.pack()


		ExtremeButton = tk.Button(self, text = "Extreme",
						command = lambda : [self.setExtreme(controller), controller.show_frame(ChooseColorPage)])

		ExtremeButton.pack()

		MasterButton = tk.Button(self, text = "Master",
						command = lambda : [self.setMaster(controller), controller.show_frame(ChooseColorPage)])

		MasterButton.pack()
	def setEasy(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 1})
	def setIntermediate(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 5})
	def setHard(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 10})
	def setExtreme(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 15})	
	def setMaster(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 20})
		
		
		
		
		
class ChoosePromotionPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Choose your promotion")
		label.pack(pady = 10, padx = 10)

		QueenButton = tk.Button(self, text = "Queen",
						command = lambda : [self.setQueen(controller)])

		RookButton = tk.Button(self, text = "Rook",
						command = lambda : [self.setRook(controller)])

		BishopButton = tk.Button(self, text = "Bishop",
						command = lambda : [self.setBishop(controller)])
	
		KnightButton = tk.Button(self, text = "Knight",
						command = lambda : [self.setKnight(controller)])
		QueenButton.pack()
		RookButton.pack()
		BishopButton.pack()
		KnightButton.pack()
		
	def setQueen(self,controller):
		controller.game.board.promotion = 'q'
		controller.game.board.move = controller.game.board.move + 'q'
		controller.game.playerPromotion(controller.game.board.move)
		if controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)
	
	def setRook(self,controller):
		controller.game.board.promotion = 'r'
		controller.game.board.move = controller.game.board.move + 'r'
		controller.game.playerPromotion(controller.game.board.move)
		if controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)
	
	
	def setBishop(self,controller):
		controller.game.board.promotion = 'b'
		controller.game.board.move = controller.game.board.move + 'b'
		controller.game.playerPromotion(controller.game.board.move)
		if controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)
	
	def setKnight(self,controller):
		controller.game.board.promotion = 'n'
		controller.game.board.move = controller.game.board.move + 'n'
		controller.game.playerPromotion(controller.game.board.move)
		if controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)
	



app = Application()
app.mainloop()
