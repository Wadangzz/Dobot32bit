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

    def start_motion(self):
        if self.api:
            dType.SetHOMECmdEx(self.api, 1, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, 250.5995, 3.0105, 148.9331, 0.6882, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, 200.8807, 0.1857, 107.9552, 0.0529, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, -30.7236, -198.5174, 107.9552, -98.7976, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, -44.631, -283.485, 75.7781, -98.9471, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, -42.7821,-281.9057, -42.8385, -99.7201, isQueued=1)
            dType.SetEndEffectorSuctionCup(self.api, 1,  1, isQueued=1)
            dType.SetWAITCmd(self.api, 200, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, -42.7821, -281.9057, 114.3617, -99.7201, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, -23.6957, -209.3128, 138.3974, -1.3689, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, 210.6473, -1.0228, 138.3974, -1.3689, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, 267.9848, -1.0227, 138.3974, -1.3689, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, 267.987, -1.0227, 91.9573, -1.3689, isQueued=1)
            dType.SetEndEffectorSuctionCup(self.api, 1,  0, isQueued=1)
            dType.SetWAITCmd(self.api, 200, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, 210.6473, -1.0228, 138.3974, -1.3689, isQueued=1)
            dType.SetPTPCmd(self.api, self.dobot_id, 250.5995, 3.0105, 148.9331, 0.6882, isQueued=1)           
            dType.SetQueuedCmdStartExec(self.api)

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
                    test.start_motion()
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
