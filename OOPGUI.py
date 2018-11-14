import tkinter as tk
from tkinter import *
from main import Game
LARGE_FONT = ("Verdana", 12)

game = Game()
moves = ["e"]

class Application(tk.Tk):

	def __init__(self,*args, **kwargs):

		tk.Tk.__init__(self,*args,**kwargs)
		container = tk.Frame(self)

		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0,weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}
		self.move = StringVar()
		self.move.set("e2")
		for F in (StartGamePage, InitializeBoardPage,SetBoardPage, ChooseColorPage,
				CPUMovePage, PlayerMovePage):

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
		label = tk.Label(self,text = "ESE 205: CV Chess", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		startGameButton = tk.Button(self, text = "Start New Game",
						command = lambda: [controller.show_frame(InitializeBoardPage), game.setUp()])
		startGameButton.pack()


class InitializeBoardPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Clear board for game set up", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		initBoardButton = tk.Button(self, text = "Done", command = lambda : [controller.show_frame(SetBoardPage), game.analyzeBoard()])
		initBoardButton.pack()

class ChooseColorPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Which color would you like to play?", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		blackButton = tk.Button(self, text = "Black",
					command = lambda : controller.show_frame(CPUMovePage))
		blackButton.pack()

		whiteButton = tk.Button(self, text = "White",
					command = lambda: controller.show_frame(PlayerMovePage))
		whiteButton.pack()

class SetBoardPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Game initialization done. Set up board", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		setBoardButton = tk.Button(self, text = "Done",
						 command = lambda : [controller.show_frame(ChooseColorPage),game.checkBoardIsSet()])
		setBoardButton.pack()

class PlayerMovePage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Your Move", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		PlayerButton = tk.Button(self, text = "Done",
						command = lambda :[ controller.show_frame(CPUMovePage),controller.move.set(game.CPUMove())])
		PlayerButton.pack()

def getMove():

	move = game.CPUMove()
	return move

class CPUMovePage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "CPU Move:", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		self.moveLabel = tk.Label(self, textvariable = controller.move, font = LARGE_FONT)
		self.moveLabel.pack(pady = 10, padx = 10)
		CPUButton = tk.Button(self, text = "Done",
						command = lambda : controller.show_frame(PlayerMovePage))
		CPUButton.pack()


def getMove():
	pass
	#controller.move.set(game.CPUMove())


app = Application()
app.mainloop()
