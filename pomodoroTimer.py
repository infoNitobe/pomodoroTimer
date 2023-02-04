# -*- coding: utf-8 -*-
import tkinter as tk
import State
class Application(tk.Frame):
	def __init__( self, master = None, state = None):
		super().__init__(master)
		master.title("pomodoro timer")
		master.geometry("550x150")
		self.pack()
		self.create_widgets()

		self.enFocus = tk.Entry(self)
		self.enFocus.grid(row = 1, column = 1)

		self._state = state

	# 部品 の 作成/ 設定
	def create_widgets(self):
		self.btSet = tk.Button(self)
		self.btSet["text"] = "設定"
		self.btSet["command"] = self.print_txtval
		self.btSet.grid(row = 0, column = 0)
		# self.enSet = tk.Entry(self)
		# self.enSet.grid(row = 1, column = 0)

		self.btFocus = tk.Button(self)
		self.btFocus["text"] = "フォーカス"
		self.btFocus["command"] = self.toFocus
		self.btFocus.grid(row = 0, column = 1)
		self.enFocus = tk.Entry(self)
		self.enFocus.grid(row = 1, column = 1)

		self.btShortRest = tk.Button(self)
		self.btShortRest["text"] = "短 休憩"
		self.btShortRest["command"] = self.print_txtval
		self.btShortRest.grid(row = 0, column = 2)
		self.enRestShort = tk.Entry(self)
		self.enRestShort.grid(row = 1, column = 2)

		self.btLongRest = tk.Button(self)
		self.btLongRest["text"] = "長 休憩"
		self.btLongRest["command"] = self.print_txtval
		self.btLongRest.grid(row = 0, column = 3)
		self.enRestLong = tk.Entry(self)
		self.enRestLong.grid(row = 1, column = 3)
	def toFocus(self):
		self._state.updateState(State.State.STATE_FORCUS)
		print("FOCUS")

	def print_txtval(self):
		val_en = self.en.get()
		print(val_en)
# root = tk.Tk()
# app = Application(master = root)
# app.mainloop()