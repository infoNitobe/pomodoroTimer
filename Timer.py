from concurrent.futures import thread
import time
import threading
import State
import tkinter as tk
from pomodoroTimer import Application
from pomodoroTimer import ConfirmationDialog
from Sound import Sound

class Timer:
    @property
    def forcusValNow(self):
        return self._forcusValNow[0]
    @property
    def shortRestValNow(self):
        return self._shortRestValNow[0]
    @property
    def longRestValNow(self):
        return self._longRestValNow[0]

    def __init__(self):
        self.st = State.State()
        self._threadFinFlag = False
        self._forcusValNow = [0]
        self._shortRestValNow = [0]
        self._longRestValNow = [0]
        self._forcusSetting = [0]
        self._shortRestSetting = [0]
        self._longRestSetting = [0]
        self._listNowVal = {self.st.STATE_FORCUS:self._forcusValNow, self.st.STATE_SHORT_REST:self._shortRestValNow, self.st.STATE_LONG_REST:self._longRestValNow}
        self._listSetting = {self.st.STATE_FORCUS:self._forcusSetting, self.st.STATE_SHORT_REST:self._shortRestSetting, self.st.STATE_LONG_REST:self._longRestSetting}
        self._listBeepFunc = {self.st.STATE_FORCUS:Sound.beep_forcus, self.st.STATE_SHORT_REST:Sound.beep_short_rest, self.st.STATE_LONG_REST:Sound.beep_long_rest}

        self.root = tk.Tk()
        self.app = Application(master = self.root, state = self.st)

        self._listEntity = {self.st.STATE_FORCUS:self.app.enFocus, self.st.STATE_SHORT_REST:self.app.enRestShort, self.st.STATE_LONG_REST:self.app.enRestLong}

        #protocol handler
        self.root.protocol("WM_DELETE_WINDOW", self.eventClose)

        self._t = threading.Thread(target = self.updateTimer)
        self._event = threading.Event()
        self._t.start()

        #この後に処理を書かないこと
        self.app.mainloop()

    def _set_values(self):
        self._forcusSetting[0] = int(self.app.enSetFocus.get())
        self._shortRestSetting[0] = int(self.app.enSetRestShort.get())
        self._longRestSetting[0] = int(self.app.enSetRestLong.get())

    def _processTransitionChk(self):
        if self.app.chkVal.get() == False:
            self.app.makeDialog()
            dialog = self.app.newDialog
            dialog.transitionFlag = True
            while dialog.transitionFlag == True:
                time.sleep(1)
    
    def _initDisplay(self, state):
        #sound
        self._listBeepFunc[state]()

        #set entity
        vals = {self.st.STATE_FORCUS:0, self.st.STATE_SHORT_REST:0, self.st.STATE_LONG_REST:0}
        vals[state] = self._listNowVal[state][0]
        self.app.enFocus.delete(0, "end")
        self.app.enFocus.insert(0, vals[self.st.STATE_FORCUS])
        self.app.enRestShort.delete(0, "end")
        self.app.enRestShort.insert(0, vals[self.st.STATE_SHORT_REST])
        self.app.enRestLong.delete(0, "end")
        self.app.enRestLong.insert(0, vals[self.st.STATE_LONG_REST])

    def _updateNowVal(self, state):
        vals = self._listNowVal[state]
        entity = self._listEntity[state]
        entity.delete(0, "end")
        entity.insert(0, vals[0])
        vals[0] -= 1
    
    def _updateValAtTimeout(self, state):
        vals = self._listNowVal[state]
        entity = self._listEntity[state]
        entity.delete(0, "end")
        entity.insert(0, vals[0])
        vals[0] = self._forcusSetting[0]
    
    def _initialNextStateVal(self, state):
        vals = self._listNowVal[state]
        settings = self._listSetting[state]
        vals[0] = settings[0]
    
    def _manageTimerAndGui(self):
        #設定状態から遷移後の処理
        if self.st.oldState == self.st.STATE_SETTING:
            self._listNowVal[self.st.nowState][0] = self._listSetting[self.st.nowState][0]
            #一度のみ、設定→特定条件への変化を検出させるため。
            self.st.forceSetOldState(self.st.nowState)
        #表示初期化
        if self._listNowVal[self.st.nowState][0] == self._listSetting[self.st.nowState][0]:
            self._initDisplay(self.st.nowState)
        #タイマー値更新
        if self._listNowVal[self.st.nowState][0] > 1:
            self._updateNowVal(self.st.nowState)
        #タイムアウトで状態更新
        elif self._listNowVal[self.st.nowState][0] == 1:
            self._updateValAtTimeout(self.st.nowState)
            self.st.updateState(None)
        
            #次の状態のタイマーの値を初期化
            self._initialNextStateVal(self.st.nowState)
            
            self._processTransitionChk()

    def eventClose(self):
        self._event.set()
        self._t.join()
        print("close Now")
        self.root.destroy()

    def updateTimer(self):
        # while not self._threadFinFlag:
        while not self._event.wait(0):
            if __debug__:
                print("not setted: wait")

            #設定状態から遷移時のタイマー値設定
            if self.st.nowState == self.st.STATE_SETTING:
                #設定
                self._set_values()

            elif self.st.nowState == self.st.STATE_FORCUS or\
                 self.st.nowState == self.st.STATE_SHORT_REST or\
                 self.st.nowState == self.st.STATE_LONG_REST:
                self._manageTimerAndGui()

            time.sleep(1)
a = Timer()
# a.updateTimer()