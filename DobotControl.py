import DobotDllType as dType
import win32com.client
import time


class Dobot():
    
    def __init__(self):

        self.CON_STR = {
            dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

        self.bot = {
            1: {
                "api": dType.load(),
                "state": None,
                "run": False,
                "isStop": False,
                "isConnected": False
            },
            2: {
                "api": dType.load(),
                "state": None,
                "run": False,
                "isStop": False,
                "isConnected": False
            },
            3: {
                "api": dType.load(),
                "state": None,
                "run": False,
                "isStop": False,
                "isConnected": False
            }
        }
        # PLC 연결
        self.plc = win32com.client.Dispatch("ActUtlType.ActUtlType")

    # PLC stationNum과 로봇 comPortNum을 인자로 받아 연결    
    def connect(self,stationNum,comPortNum):

        # 로봇 원호보간 모드
        movj = dType.PTPMode.PTPMOVJXYZMode

        bot = self.bot[stationNum]
        api = bot["api"]
            
        self.plc.ActLogicalStationNumber = stationNum
        if self.plc.Open() == 0:

            print('연결 성공')
            bot["isConnected"] = True
            bot["state"] = dType.ConnectDobot(api, f"COM{comPortNum}", 115200)[0]
            # 로봇 연결 성공 시
            if bot["state"] == dType.DobotConnect.DobotConnect_NoError:
                # 로봇 초기화
                dType.SetQueuedCmdClear(api)
                dType.SetHOMEParams(api, -0.7725620269775391, -202.97116088867188, 114.29161834716797, 0, isQueued = 1)
                dType.SetPTPJointParams(api, 100, 100, 100, 100, 150, 150, 150, 150, isQueued = 1)
                dType.SetPTPCommonParams(api, 90, 90, isQueued = 1)
                dType.SetARCCommonParams(api, 200, 200, isQueued = 1)
                dType.SetHOMECmdEx(api, 1, isQueued=1)
                # 로봇에 따라 위치 다르게 설정
                if stationNum == 1:
                    dType.SetPTPCmd(api, movj, 193.80259704589844, -91.76068115234375, 73.77569580078125, 64.2706069946289, isQueued=1)
                elif stationNum == 3:
                    dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
    
    # PLC stationNum과 로봇 comPortNum을 인자로 받아 연결 해제    
    def disconnect(self,stationNum):

        bot = self.bot[stationNum]
        api = bot["api"]
        dType.DisconnectDobot(api)
        print('로봇 연결 해제 완료')

        if self.plc.Close() == 0:
            bot["isConnected"] = False

            print('PLC 연결 해제 완료')

    def GetPose(self,stationNum):
        bot = self.bot[stationNum]
        api = bot["api"]

        return [stationNum,
            dType.GetPose(api)[4],
            dType.GetPose(api)[5],
            dType.GetPose(api)[6],
            dType.GetPose(api)[7]]
            
    # 로봇 원점 복귀 함수
    def Home(self,stationNum):
        movj = dType.PTPMode.PTPMOVJXYZMode
        if stationNum not in self.bot:
            raise ValueError(f"Invalid station number: {stationNum}")
            
        api = self.bot[stationNum]["api"]
        dType.SetHOMEParams(api, -0.7725620269775391, -202.97116088867188, 114.29161834716797, 0, isQueued = 0)
        dType.SetPTPJointParams(api, 100, 100, 100, 100, 150, 150, 150, 150, isQueued = 0)
        dType.SetPTPCommonParams(api, 90, 90, isQueued = 0)
        dType.SetARCCommonParams(api, 200, 200, isQueued = 0)
        dType.SetHOMECmdEx(api, 1, isQueued=0)
        if stationNum == 1:
            dType.SetPTPCmd(api, movj, 193.80259704589844, -96.20050811767578, 73.77569580078125, 64.2706069946289, isQueued=0)
        elif stationNum == 3:
            dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=0) 

    # stationNum에 따라 로봇을 제어하는 함수
    def robot(self, stationNum, device):
        movj = dType.PTPMode.PTPMOVJXYZMode
        movl = dType.PTPMode.PTPMOVLXYZMode

        if stationNum not in self.bot:
            raise ValueError(f"Invalid station number: {stationNum}")
            
        bot = self.bot[stationNum]
        api = bot["api"]
        
        if bot["state"] != dType.DobotConnect.DobotConnect_NoError:
            return

        # Jupyter Notebook으로 로봇 Teaching하여 생성한 경로를 따라 이동
        # Station 1 specific movements
        if stationNum == 1:

            dType.SetPTPCmd(api, movj, 193.80259704589844, -96.20050811767578, 73.77569580078125, 64.2706069946289, isQueued=1) 
            dType.SetPTPCmd(api, movl, 193.80259704589844, -96.20050811767578, 14.255363464355469, 64.27061462402344, isQueued=1)
            dType.SetPTPCmd(api, movl, 193.80259704589844, -96.20050811767578, 14.255363464355469, 64.27061462402344, isQueued=1)
            dType.SetWAITCmd(api, 250, isQueued=1)
            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
            dType.SetWAITCmd(api, 250, isQueued=1)
            dType.SetPTPCmd(api, movj, 193.80259704589844, -96.20050811767578, 73.77569580078125, 64.2706069946289, isQueued=1)
            dType.SetPTPCmd(api, movj, 5.596028757095337, -251.3144073486328, 60.001197814941406, -27.571914672851562, isQueued=1)

            # device에 따라 달라지는 부분
            if device == 0:
                dType.SetPTPCmd(api, movj, 5.596028757095337, -267.60247802734375, 40.00385284423828, -27.571914672851562, isQueued=1)
                dType.SetPTPCmd(api, movl, 5.596034049987793, -267.6034240722656, 25.62419891357422, -27.571914672851562, isQueued=1)
            elif device == 1:
                dType.SetPTPCmd(api, movl, 5.594710826873779, -288.94573974609375, 60.204517364501953, -27.571914672851562, isQueued=1)
                dType.SetPTPCmd(api, movl, 4.594710826873779, -288.94573974609375, 28.204517364501953, -27.571914672851562, isQueued=1)

            dType.SetWAITCmd(api, 250, isQueued=1)
            dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
            dType.SetWAITCmd(api, 250, isQueued=1)
            dType.SetPTPCmd(api, movl, 5.596028757095337, -251.3144073486328, 60.001197814941406, -27.571914672851562, isQueued=1)

        # Station 2 specific movements
        elif stationNum == 2:
            if device == 0:
                dType.SetPTPCmd(api, movl, 5.582981109619141, -203.95887756347656, 156.9364013671875, 0, isQueued=1) 
                dType.SetPTPCmd(api, movl, 5.582981109619141, -203.95887756347656, 156.9364013671875, 0, isQueued=1) 
                dType.SetPTPCmd(api, movl, 5.582981109619141, -258.56048583984375, 156.9364013671875, 0, isQueued=1)    
                dType.SetPTPCmd(api, movl, 5.582981109619141, -258.56048583984375, 150.9364013671875, 0, isQueued=1)    
                dType.SetWAITCmd(api, 250, isQueued=1)
                gripIndex1 = dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)[0]
                dType.SetWAITCmd(api, 1500, isQueued=1)
                dType.SetPTPCmd(api, movl, 5.582981109619141, -258.56048583984375, 156.9364013671875, 0, isQueued=1)    
                dType.SetPTPCmd(api, movj, 5.582981109619141, -196.79473876953125, 156.9364013671875, 0, isQueued=1)    
                dType.SetARCCmd(api, [75.353515625, -181.7982940673828, 152.9364013671875, 22.73912811279297], 
                                [196.90408325195312, -2.6424760818481445, 40.249359130859375, 89.40617370605469], isQueued=1 )
                dType.SetPTPCmd(api, movl, 196.90408325195312, -2.6424760818481445, 21.2576806640625, 89.40617370605469, isQueued=1)
                dType.SetWAITCmd(api, 250, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)
                gripIndex2 = dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)[0]
                dType.SetWAITCmd(api, 1500, isQueued=1)
                dType.SetPTPCmd(api, movl, 196.90408325195312, -2.6424760818481445, 50.249359130859375, 89.40617370605469, isQueued=1)

            elif device == 1: # 로봇 2는 외부 공압 컴프레셔에서 그리퍼 연결해서 사용함함
                dType.SetPTPCmd(api, movj, -0.7725620269775391, -204.97116088867188, 114.29161834716797, 0 , isQueued=1)
                dType.SetPTPCmd(api, movj, 59.901798248291016, -196.02142333984375, 114.29156494140625, 17.208480834960938 , isQueued=1) 
                dType.SetARCCmd(api, [138.06761169433594, -140.7730255126953, 80.834869384765625, 44.66006088256836], 
                                [186.84396362304688, -3.5974104404449463, 50.2476806640625, 89.40254211425781], isQueued=1 )
                dType.SetPTPCmd(api, movl, 186.84384155273438, -3.5974104404449463, 17.12774658203125, 89.40254211425781, isQueued=1)
                dType.SetWAITCmd(api, 250, isQueued=1)
                gripIndex1 = dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)[0]
                dType.SetWAITCmd(api, 1500, isQueued=1)
                dType.SetPTPCmd(api, movl, 186.84384155273438, -3.0974104404449463, 70.12774658203125, 89.40254211425781, isQueued=1)
                dType.SetPTPCmd(api, movl, 290.84384155273438, -3.0974104404449463, 70.12774658203125, 89.40254211425781, isQueued=1)
                dType.SetWAITCmd(api, 250, isQueued=1)
                gripIndex2 = dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)[0]
                dType.SetWAITCmd(api, 1500, isQueued=1)
                dType.SetPTPCmd(api, movl, 186.84384155273438, -3.0974104404449463, 70.12774658203125, 89.40254211425781, isQueued=1)

        # Station 3 specific movements
        elif stationNum == 3:
            if device in [1, 2, 4]:
                dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
                dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
                dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1)
                dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1)   
                dType.SetWAITCmd(api, 250, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
                dType.SetWAITCmd(api, 250, isQueued=1)
                dType.SetPTPCmd(api, movl, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1)    

                if device == 1:
                    dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 100.88801574707031, 112.61143493652344], 
                                    [55.460655212402344, 224.66812133789062, 100.73353576660156, 183.70411682128906], isQueued=1 )
                    dType.SetPTPCmd(api, movl, 55.46128463745117, 224.67137145996094, 68.33453369140625, 183.7054901123047, isQueued=1)
                    dType.SetWAITCmd(api, 250, isQueued=1)
                    dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                    dType.SetWAITCmd(api, 250, isQueued=1)
                    dType.SetPTPCmd(api, movl, 55.46128463745117, 224.67137145996094, 100.73353576660156, 183.7054901123047, isQueued=1)
                elif device == 2:
                    dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
                                    [6.500369548797607, 223.6554718017578, 100.73333740234375, 182.9855194091797], isQueued=1 )
                    dType.SetPTPCmd(api, movl, 6.500369548797607, 223.6554718017578, 68.33453369140625, 182.9855194091797, isQueued=1)
                    dType.SetWAITCmd(api, 250, isQueued=1)
                    dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                    dType.SetWAITCmd(api, 250, isQueued=1)
                    dType.SetPTPCmd(api, movl, 6.500369548797607, 223.6554718017578, 100.73333740234375, 182.9855194091797, isQueued=1)
                elif device == 4:
                    dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
                                    [-41.87975311279297, 224.66201782226562, 100.73306274414062, 182.98736572265625], isQueued=1 )
                    dType.SetPTPCmd(api, movl, -41.87975311279297, 224.66201782226562, 68.33453369140625, 182.98736572265625, isQueued=1)
                    dType.SetWAITCmd(api, 250, isQueued=1)
                    dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                    dType.SetWAITCmd(api, 250, isQueued=1)
                    dType.SetPTPCmd(api, movl, -41.87975311279297, 224.66201782226562, 100.73306274414062, 182.98736572265625, isQueued=1)
                
                dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 100.88801574707031, 112.61143493652344], 
                                [259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344], isQueued=1 )

        # Common execution logic
        if stationNum == 1:
            lastIndex = dType.SetPTPCmd(api, movj, 193.80259704589844, -96.20050811767578, 73.77569580078125, 64.2706069946289, isQueued=1)[0]
        elif stationNum == 2:
            lastIndex = dType.SetPTPCmd(api, movj, -0.7725620269775391, -204.97116088867188, 114.29161834716797, 0, isQueued=1)[0]
        elif stationNum == 3:
            lastIndex = dType.SetPTPCmd(api, movj, 259.4306335449219, 23.712833404541016, 81.51910400390625, 91.5084228515625, isQueued=1)[0]
        
        # Teaching한 경로를 순서대로 Dequeue하여 로봇 동작한다
        dType.SetQueuedCmdStartExec(api)

        while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
            stop_flag = f"M{200 + stationNum - 1}"
            if not bot["isStop"] and self.plc.GetDevice(stop_flag)[1] == 1:
                bot["isStop"] = True
                dType.SetQueuedCmdStopExec(api)
            elif bot["isStop"] and self.plc.GetDevice(stop_flag)[1] == 0:
                bot["isStop"] = False
                dType.SetQueuedCmdStartExec(api)

            if self.plc.GetDevice("X21A")[1] == 1:
                dType.SetQueuedCmdClear(api)
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=0)
                if stationNum == 2: # 로봇 2는 공압 그리퍼까지 OFF
                    self.plc.SetDevice("M205", 1)
                    time.sleep(0.01)
                    self.plc.SetDevice("M205", 0)
                break

            if stationNum == 2:
                if dType.GetQueuedCmdCurrentIndex(api)[0] == gripIndex1:
                    self.plc.SetDevice("M203", 1)
                    time.sleep(0.01)
                    self.plc.SetDevice("M203", 0)
                elif dType.GetQueuedCmdCurrentIndex(api)[0] == gripIndex2:
                    self.plc.SetDevice("M205", 1)
                    time.sleep(0.01)
                    self.plc.SetDevice("M205", 0)

            dType.dSleep(1000)

        bot["run"] = False