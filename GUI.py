import tkinter as tk
from testEngine import testEngine

class Application(tk.Frame):

	def __init__(self,master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):

		self.hi = tk.Button(self)
		self.hi["text"] = "Start New Game"
		self.hi["command"] = self.say_hi
		self.hi.pack(side ="top")

		self.quit = tk.Button(self,text="QUIT", fg = "red", command = self.master.destroy)

		self.quit.pack(side = "bottom")

	def say_hi(self):

		testEngine()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
