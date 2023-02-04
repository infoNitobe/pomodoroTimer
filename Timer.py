from concurrent.futures import thread
import time
import threading
import State
import tkinter as tk
from pomodoroTimer import Application

class Timer:
    FORCUS_DEFALT_VAL = 3
    SHORT_REST_DEFALT_VAL = 1
    LONG_REST_DEFALT_VAL = 2
    def __init__(self):
        self._threadFinFlag = False
        self._forcusSetting = self.FORCUS_DEFALT_VAL
        self._shortRestSetting = self.SHORT_REST_DEFALT_VAL
        self._longRestSetting = self.LONG_REST_DEFALT_VAL

        self._forcusValNow = 0
        self._shortRestValNow = 0
        self._longRestValNow = 0

        self.st = State.State()
        self._t = threading.Thread(target = self.updateTimer)
        self._event = threading.Event()
        self._t.start()

        self.root = tk.Tk()
        self.app = Application(master = self.root, state = self.st)
        #protocol handler
        self.root.protocol("WM_DELETE_WINDOW", self.eventClose)

        #この後に処理を書かないこと
        self.app.mainloop()

    @property
    def forcusValNow(self):
        return self._forcusValNow
    @property
    def shortRestValNow(self):
        return self._shortRestSetting
    @property
    def longRestValNow(self):
        return self._longRestSetting

    def eventClose(self):
        self._event.set()
        self._t.join()
        print("close Now")
        self.root.destroy()

#todo:
#   途中で設定できるようにする。
    def updateTimer(self):
        # while not self._threadFinFlag:
        while not self._event.wait(0):
            if __debug__:
                print("not setted: wait")

            #設定状態から遷移時のタイマー値設定
            if self.st.oldState == self.st.STATE_SETTING:
                if self.st.nowState == self.st.STATE_FORCUS:
                    self._forcusValNow = self._forcusSetting
                elif self.st.nowState == self.st.STATE_SHORT_REST:
                    self._forcusValNow = self._shortRestSetting
                elif self.st.nowState == self.st.STATE_LONG_REST:
                    self._forcusValNow = self._longRestSetting
                #一度のみ、設定→特定条件への変化を検出させるため。
                self.st.forceSetOldState(self.st.nowState)

            if self.st._nowState == self.st.STATE_FORCUS:
                #表示初期化
                #HACK: enFocusにforcuSettingを表示させる処理はタイマー値更新と被る。可能なら修正。但し、単純にelifにするとforcusSettingに1を設定した時に上手くいかなくなる。
                if self._forcusValNow == self._forcusSetting:
                    self.app.enFocus.delete(0, "end")
                    self.app.enFocus.insert(0, self._forcusValNow)
                    self.app.enRestShort.delete(0, "end")
                    self.app.enRestShort.insert(0, 0)
                    self.app.enRestLong.delete(0, "end")
                    self.app.enRestLong.insert(0, 0)
                #タイマー値更新
                if self._forcusValNow > 1:
                    self.app.enFocus.delete(0, "end")
                    self.app.enFocus.insert(0, self._forcusValNow)
                    self._forcusValNow -= 1
                #タイムアウトで状態更新
                elif self._forcusValNow == 1:
                    self.app.enFocus.delete(0, "end")
                    self.app.enFocus.insert(0, self._forcusValNow)
                    self._forcusValNow = self._forcusSetting
                    self.st.updateState(None)
                
                    #次の状態のタイマーの値を初期化
                    if self.st.nowState == self.st.STATE_SHORT_REST:
                        self._shortRestValNow = self._shortRestSetting
                    elif self.st.nowState == self.st.STATE_LONG_REST:
                        self._longRestValNow = self._longRestSetting

            elif self.st.nowState == self.st.STATE_SHORT_REST:
                #表示初期化
                if self._shortRestValNow == self._shortRestSetting:
                    self.app.enFocus.delete(0, "end")
                    self.app.enFocus.insert(0, 0)
                    self.app.enRestShort.delete(0, "end")
                    self.app.enRestShort.insert(0, self._shortRestValNow)
                    self.app.enRestLong.delete(0, "end")
                    self.app.enRestLong.insert(0, 0)
                #タイマー値更新
                if self._shortRestValNow > 1:
                    self.app.enRestShort.delete(0, "end")
                    self.app.enRestShort.insert(0, self._shortRestValNow)
                    self._shortRestValNow -= 1
                #タイムアウトで状態更新
                elif self._shortRestValNow == 1:
                    self.app.enRestShort.delete(0, "end")
                    self.app.enRestShort.insert(0, self._shortRestValNow)
                    self._shortRestValNow = self._shortRestSetting
                    self.st.updateState(None)
                
                    #次の状態のタイマーの値を初期化
                    self._forcusValNow = self._forcusSetting
        
            elif self.st.nowState == self.st.STATE_LONG_REST:
                #表示初期化
                if self._longRestValNow == self._longRestSetting:
                    self.app.enFocus.delete(0, "end")
                    self.app.enFocus.insert(0, 0)
                    self.app.enRestShort.delete(0, "end")
                    self.app.enRestShort.insert(0, 0)
                    self.app.enRestLong.delete(0, "end")
                    self.app.enRestLong.insert(0, self._longRestValNow)
                #タイマー値更新
                if self._longRestValNow > 1:
                    self.app.enRestLong.delete(0, "end")
                    self.app.enRestLong.insert(0, self._longRestValNow)
                    self._longRestValNow -= 1
                #タイムアウトで状態更新
                elif self._longRestValNow == 1:
                    self.app.enRestLong.delete(0, "end")
                    self.app.enRestLong.insert(0, self._longRestValNow)
                    self._longRestValNow = self._longRestSetting
                    self.st.updateState(None)
                
                    #次の状態のタイマーの値を初期化
                    self._longRestValNow = self._longRestSetting
            time.sleep(1)
a = Timer()
# a.updateTimer()