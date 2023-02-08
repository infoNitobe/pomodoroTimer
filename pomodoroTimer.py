# -*- coding: utf-8 -*-
import tkinter as tk
import State
class Application(tk.Frame):
	FORCUS_DEFALT_VAL = 3
	SHORT_REST_DEFALT_VAL = 1
	LONG_REST_DEFALT_VAL = 2
	def __init__( self, master = None, state = None):
		super().__init__(master)
		master.title("pomodoro timer")
		master.geometry("550x150")
		self.pack()
		self.create_widgets()

		self._state = state

	# 部品 の 作成/ 設定
	def create_widgets(self):
		#line 1
		#forcus
		self.btFocus = tk.Button(self)
		self.btFocus["text"] = "フォーカス"
		self.btFocus["command"] = self.toFocus
		self.btFocus.grid(row = 0, column = 1)
		#短　休憩
		self.btShortRest = tk.Button(self)
		self.btShortRest["text"] = "短 休憩"
		self.btShortRest["command"] = self.toShortRest
		self.btShortRest.grid(row = 0, column = 2)
		#長　休憩
		self.btLongRest = tk.Button(self)
		self.btLongRest["text"] = "長 休憩"
		self.btLongRest["command"] = self.toLongRest
		self.btLongRest.grid(row = 0, column = 3)
		#チェックボタン：画面遷移
		self.chkVal = tk.BooleanVar(self)
		self.chkB = tk.Checkbutton(self, variable=self.chkVal, text="画面遷移")
		self.chkB.grid(row = 0, column = 4)

		#line2
		#label
		self.lbSetting = tk.Label(self)
		self.lbSetting["text"] = "設定値"
		self.lbSetting.grid(row = 1, column = 0)
		#forcus
		self.enSetFocus = tk.Entry(self)
		self.enSetFocus.insert(0, str(self.FORCUS_DEFALT_VAL))
		self.enSetFocus.grid(row = 1, column = 1)
		#短　休憩
		self.enSetRestShort = tk.Entry(self)
		self.enSetRestShort.insert(0, str(self.SHORT_REST_DEFALT_VAL))
		self.enSetRestShort.grid(row = 1, column = 2)
		#長　休憩
		self.enSetRestLong = tk.Entry(self)
		self.enSetRestLong.insert(0, str(self.LONG_REST_DEFALT_VAL))
		self.enSetRestLong.grid(row = 1, column = 3)

		#line3
		#label
		self.lbCurrent = tk.Label(self)
		self.lbCurrent["text"] = "現在値"
		self.lbCurrent.grid(row = 2, column = 0)
		#forcus
		self.enFocus = tk.Entry(self)
		self.enFocus.grid(row = 2, column = 1)
		#短　休憩
		self.enRestShort = tk.Entry(self)
		self.enRestShort.grid(row = 2, column = 2)
		#長　休憩
		self.enRestLong = tk.Entry(self)
		self.enRestLong.grid(row = 2, column = 3)

	def toFocus(self):
		self._state.updateState(State.State.STATE_FORCUS)
		print("FOCUS")

	def toShortRest(self):
		self._state.updateState(State.State.STATE_SHORT_REST)
		print("SHORT_REST")
	
	def toLongRest(self):
		self._state.updateState(State.State.STATE_LONG_REST)
		print("LONG_REST")

	def makeDialog(self):
		self.newWindow = tk.Toplevel(self.master)
		self.newDialog = ConfirmationDialog(self.newWindow)

class ConfirmationDialog(tk.Frame):
	transitionFlag = False
	def __init__( self, master = None):
		super().__init__(master)
		self.pack()
		self.master.title("confirmation dialog")
		self.master.geometry("150x150")
		self.create_widgets()
	
	def _clearTransitionFlag(self):
		self.transitionFlag = False
		self.master.destroy()

	# 部品 の 作成/ 設定
	def create_widgets(self):
		self.bt = tk.Button(self)
		self.bt["text"] = "OK"
		self.bt["command"] = self._clearTransitionFlag
		self.bt.pack()
	