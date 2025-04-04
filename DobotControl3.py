import DobotDllType as dType
import win32com.client

class Dobot():

    def __init__(self):

        self.CON_STR = {
            dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

        self.api = dType.load()
        self.state = None
        self.run = False

        self.plc = win32com.client.Dispatch("ActUtlType.ActUtlType")
        self.plc.ActLogicalStationNumber = 0
        if self.plc.Open() == 0:
            print('연결 성공')
        
    def Estop(self):
            
            self.isStop == True
            dType.SetQueuedCmdStopExec(self.api)
            return 1
        
    def restart(self):
            
            self.isStop = False
            dType.SetQueuedCmdStartExec(self.api)
            return 0
        
    def connect(self,_num):

        api = self.api
        # Dobot 연결 (USB 포트)
        self.state = dType.ConnectDobot(api, f"COM{_num}", 115200)[0]
        print("Connect status:",self.CON_STR[self.state])
        if (self.state == dType.DobotConnect.DobotConnect_NoError):
            # Dobot의 명령 큐 초기화
            dType.SetQueuedCmdClear(api)
            dType.SetHOMEParams(api, 200, -100, 100, 0, isQueued = 1)
            dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
            dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
            dType.SetARCCommonParams(api, 100, 100, isQueued = 1)
            dType.SetPTPJumpParams(api, jumpHeight=20, zLimit=150, isQueued=1)
            dType.SetHOMECmdEx(api, 1, isQueued=1)
            dType.SetQueuedCmdStartExec(api)

    def demotest(self,_Device):
        
        isStop = False
        api = self.api

        pick_point = {"x": 220, "y": 0, "z": -20, "r": 0}   # Pick 좌표
        place_point = {"x": 250, "y": 100, "z": -20, "r": 0} # Place 좌표
        safe_z = 30  # 안전 높이

       
        if (self.state == dType.DobotConnect.DobotConnect_NoError):
            
            # Dobot의 명령 큐 초기화
            # dType.SetQueuedCmdClear(api)
            
            # # Home 위치 및 모션 파라미터 설정
            # dType.SetHOMEParams(api, 200, 200, 200, 200, isQueued = 1)
            # dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
            # dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
            # dType.SetARCCommonParams(api, 100, 100, isQueued = 1)
            # dType.SetPTPJumpParams(api, jumpHeight=20, zLimit=150, isQueued=1)


            # #Async PTP Motion
            # for i in range(0, 5):
            #     if i % 2 == 0:
            #         offset = 50
            #     else:
            #         offset = -50
            #     lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 200 + offset, offset, offset, offset, isQueued = 1)[0]
                
            if _Device == 100:

                # 1. Pick 작업
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, pick_point["x"], pick_point["y"], safe_z, pick_point["r"], isQueued=1)  # 접근
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, pick_point["x"], pick_point["y"], pick_point["z"], pick_point["r"], isQueued=1)  # 하강
                dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, pick_point["x"], pick_point["y"], safe_z, pick_point["r"], isQueued=1)  # 다시 상승

                # 2. Place 작업
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, place_point["x"], place_point["y"], safe_z, place_point["r"], isQueued=1)  # 접근
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, place_point["x"], place_point["y"], place_point["z"], place_point["r"], isQueued=1)  # 하강
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, place_point["x"], place_point["y"], safe_z, place_point["r"], isQueued=1)  # 다시 상승
            
            elif _Device == 0:

                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 154.8227, 16.3688, 23.9239, 6.0314, isQueued=1)
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 195.3818, 95.8283, 74.2508, 26.1225, isQueued=1) 
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 236.1482, 19.1341, 150.7897, 4.6284, isQueued=1)  
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 165.6623, -118.2687, 77.2369, -35.5275, isQueued=1)
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 212.2959, -136.5227, -32.5332, 0, isQueued=1)
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 212.2959, -136.5227, -52.5332, 0, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 212.2959, -136.5227, -32.5332, 0, isQueued=1)
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 165.6623, -118.2687, 77.2369, -35.5275, isQueued=1)
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 236.1482, 19.1341, 150.7897, 4.6284, isQueued=1) 
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 195.3818, 95.8283, 74.2508, 26.1225, isQueued=1) 
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 154.8227, 16.3688, 23.9239, 6.0314, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 195.3818, 95.8283, 74.2508, 26.1225, isQueued=1) 

            lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 220 , 0 , -20, 0 , isQueued=1)[0] 

            #Start to Execute Command Queue
            dType.SetQueuedCmdStartExec(api)

            while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                if self.plc.GetDevice("M200")[1] == 1:
                    isStop = True
                    dType.SetQueuedCmdStopExec(api)
                elif isStop and self.plc.GetDevice("M200")[1] == 0:
                    isStop = False
                    dType.SetQueuedCmdStartExec(api)
                dType.dSleep(1000)

            dType.SetQueuedCmdStopExec(api)

            self.run = False
            #Stop to Execute Command Queued
            # 
        #Disconnect Dobot
        # dType.DisconnectDobot(api)