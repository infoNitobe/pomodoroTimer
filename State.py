class State:
    STATE_SETTING = "setting"
    STATE_FORCUS = "forcus"
    STATE_SHORT_REST = "shortRest"
    STATE_LONG_REST = "longRest"

    def __init__(self):
        self._nowState = self.STATE_SETTING
        self._oldState = ""
        self._numShortRestSetting = 2
        self._numShortRestNow = 2
    
    @property
    def nowState(self):
        return self._nowState
    
    @property
    def oldState(self):
        return self._oldState
    
    def updateState(self, specifiedState):
        if self.nowState == self.STATE_SETTING:
            self._oldState = self._nowState
            self._nowState = specifiedState
        elif self.nowState == self.STATE_FORCUS:
            if self._numShortRestNow > 0:
                self._oldState = self._nowState
                self._nowState = self.STATE_SHORT_REST
            else:
                self._numShortRestNow = self._numShortRestSetting
                self._oldState = self._nowState
                self._nowState = self.STATE_LONG_REST
        elif self.nowState == self.STATE_SHORT_REST:
            self._numShortRestNow -= 1
            self._oldState = self._nowState
            self._nowState = self.STATE_FORCUS
        elif self.nowState == self.STATE_LONG_REST:
            self._oldState = self._nowState
            self._nowState = self.STATE_FORCUS
    
    def forceSetOldState(self, state):
        self._oldState = state

    def forceSetting(self):
        self._oldState = self._nowState
        self._nowState = self.STATE_SETTING

