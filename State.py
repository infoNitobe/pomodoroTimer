class State:
    STATE_SETTING = "setting"
    STATE_FORCUS = "forcus"
    STATE_SHORT_REST = "shortRest"
    STATE_LONG_REST = "longRest"

    def __init__(self):
        self._nowState = self.STATE_SETTING
        self._oldState = ""
        self._numShortRestSetting = 3
        self._numShortRestNow = 3
    
    @property
    def nowState(self):
        return self._nowState
    
    @property
    def oldState(self):
        return self._oldState
    
    def updateState(self, nowState):
        if self._nowState == self.STATE_SETTING:
            self._oldState = self._nowState
            self._nowState = nowState
        elif self._nowState == self.STATE_FORCUS:
            if self._numShortRestNow > 0:
                self._numShortRestNow -= 1
                self._oldState = self._nowState
                self._nowState = self.STATE_SHORT_REST
            else:
                self._numShortRestNow = self._numShortRestSetting
                self._oldState = self._nowState
                self._nowState = self.STATE_LONG_REST
        elif self._nowState == self.STATE_SHORT_REST:
            self._oldState = self._nowState
            self._nowState = self.STATE_FORCUS
        elif self._nowState == self.STATE_LONG_REST:
            self._oldState = self._nowState
            self._nowState = self.STATE_FORCUS
    
    def forceSetOldState(self, state):
        self._oldState = state

