import threading
import DobotDllType as dType
import win32com.client
import time

class Dobot():
    def __init__(self):
        self.api = None
        self.dobot_id = dType.PTPMode.PTPMOVJXYZMode
        self.is_paused = False
        
    def connect_dobot(self, _num):
        self.api = dType.load()
        state = dType.ConnectDobot(self.api, f"COM{_num}", 115200)[0]
        return state
    
    def setup_dobot(self):
        if self.api:
            dType.SetQueuedCmdClear(self.api)
            dType.SetHOMEParams(self.api, 230.9534, -56.5766, 115.8194, -13.7647, isQueued=1)
            dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued=1)
            dType.SetPTPCommonParams(self.api, 50, 50, isQueued=1)
            dType.SetARCCommonParams(self.api, 50, 50, isQueued=1)
            dType.SetPTPJumpParams(self.api, jumpHeight=20, zLimit=150, isQueued=1)

    def start_motion(self, plc):
        if self.api:
            dType.SetHOMECmd(self.api, 1, 0)
            dType.SetPTPCmd(self.api, self.dobot_id, 230.9534, -56.5766, 115.8194, -13.7647, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, 41.3073, -235.3951, 110.6912, -80.047, isQueued=1)
            lastIndex = dType.SetPTPCmd(self.api, self.dobot_id, 220, 0, -20, 0, isQueued=1)[0]
            dType.SetQueuedCmdStartExec(self.api)
            
            while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                dType.dSleep(1000)
            
            dType.SetQueuedCmdStopExec(self.api)
            plc.SetDevice("M2", 1)
            print("Motion Complete, M2 Set to 1")

    def pause_motion(self):
        if self.api and not self.is_paused:
            dType.SetQueuedCmdStopExec(self.api)
            self.is_paused = True
            print("Dobot Paused")
    
    def resume_motion(self):
        if self.api and self.is_paused:
            dType.SetQueuedCmdStartExec(self.api)
            self.is_paused = False
            print("Dobot Resumed")
    
    def disconnect_dobot(self):
        if self.api:
            dType.DisconnectDobot(self.api)
            print("Dobot Disconnected")

if __name__ == "__main__":
    test = Dobot()
    plc = win32com.client.Dispatch("ActUtlType.ActUtlType")
    plc.ActLogicalStationNumber = 6
    
    if plc.Open() == 0:
        print('PLC 연결 성공')
        num = 3
        if test.connect_dobot(num) == dType.DobotConnect.DobotConnect_NoError:
            test.setup_dobot()
            
            while True:
                run = plc.GetDevice("M0")[1]
                pause = plc.GetDevice("M1")[1]
                
                if run == 1:
                    test.start_motion(plc)
                    plc.SetDevice("M0", 0)
                
                if pause == 1:
                    test.pause_motion()
                else:
                    test.resume_motion()
                
                time.sleep(1)
        else:
            print("Dobot 연결 실패")
    else:
        print('PLC 연결 실패')
