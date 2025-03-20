import threading
import DobotDllType as dType

class Dobot():

    def demotest(self,_num):


        pick_point = {"x": 220, "y": 0, "z": -20, "r": 0}   # Pick 좌표
        place_point = {"x": 250, "y": 100, "z": -20, "r": 0} # Place 좌표
        safe_z = 30  # 안전 높이

        CON_STR = {
            dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

        # Dobot DLL 로드 및 API 핸들 가져오기
        api = dType.load()

        # Dobot 연결 (USB 포트)
        state = dType.ConnectDobot(api, f"COM{_num}", 115200)[0]
        print("Connect status:",CON_STR[state])

        if (state == dType.DobotConnect.DobotConnect_NoError):
            
            # Dobot의 명령 큐 초기화
            dType.SetQueuedCmdClear(api)
            
            # Home 위치 및 모션 파라미터 설정
            dType.SetHOMEParams(api, 100, 100, 100, 100, isQueued = 1)
            dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
            dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
            dType.SetARCCommonParams(api, 100, 100, isQueued = 1)
            dType.SetPTPJumpParams(api, jumpHeight=20, zLimit=150, isQueued=1)



            # #Async PTP Motion
            # for i in range(0, 5):
            #     if i % 2 == 0:
            #         offset = 50
            #     else:
            #         offset = -50
            #     lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 200 + offset, offset, offset, offset, isQueued = 1)[0]
                # 1. Pick 작업
            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, pick_point["x"], pick_point["y"], safe_z, pick_point["r"], isQueued=1)  # 접근
            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, pick_point["x"], pick_point["y"], pick_point["z"], pick_point["r"], isQueued=1)  # 하강
            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, pick_point["x"], pick_point["y"], safe_z, pick_point["r"], isQueued=1)  # 다시 상승

            # 2. Place 작업
            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, place_point["x"], place_point["y"], safe_z, place_point["r"], isQueued=1)  # 접근
            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, place_point["x"], place_point["y"], place_point["z"], place_point["r"], isQueued=1)  # 하강
            dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, place_point["x"], place_point["y"], safe_z, place_point["r"], isQueued=1)  # 다시 상승
                    # #Async Home
            lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 220 , 0 , -20, 0 , isQueued=1)[0] 

            #Start to Execute Command Queue
            dType.SetQueuedCmdStartExec(api)

            #Wait for Executing Last Command 
            while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                dType.dSleep(1000)

            #Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(api)

        #Disconnect Dobot
        dType.DisconnectDobot(api)
