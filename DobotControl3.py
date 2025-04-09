import DobotDllType as dType
import win32com.client
import time


class Dobot():

    def __init__(self):

        self.CON_STR = {
            dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

        self.api1 = dType.load()
        self.api2 = dType.load()
        self.api3 = dType.load()
        self.state1 = None
        self.state2 = None
        self.state3 = None
        self.run1 = False
        self.run2 = False
        self.run3 = False
        self.isStop1 = False
        self.isStop2 = False
        self.isStop3 = False
        self.isConnected1 = False
        self.isConnected2= False
        self.isConnected3 = False
        self.plc = win32com.client.Dispatch("ActUtlType.ActUtlType")
        
    def connect(self,stationNum,_num):

        movj = dType.PTPMode.PTPMOVJXYZMode
        movl =dType.PTPMode.PTPMOVLXYZMode

        if stationNum == 1:
            api = self.api1
        elif stationNum == 2:
            api = self.api2
        elif stationNum == 3:
            api = self.api3
            
        self.plc.ActLogicalStationNumber = stationNum
        if self.plc.Open() == 0:
            print('연결 성공')
            if stationNum == 1:
                self.isConnected1 = True
            elif stationNum == 2:
                self.isConnected2 = True
            elif stationNum == 3:
                self.isConnected3 = True
            
            # Dobot 연결 (USB 포트)
            if stationNum == 1:
                self.state1 = dType.ConnectDobot(api, f"COM{_num}", 115200)[0]
                state = self.state1
            elif stationNum == 2:
                self.state2 = dType.ConnectDobot(api, f"COM{_num}", 115200)[0]
                state = self.state2
            elif stationNum == 3:
                self.state3 = dType.ConnectDobot(api, f"COM{_num}", 115200)[0]
                state = self.state3
        
            if (state == dType.DobotConnect.DobotConnect_NoError):
                # Dobot의 명령 큐 초기화
                dType.SetQueuedCmdClear(api)
                dType.SetHOMEParams(api, -0.7725620269775391, -202.97116088867188, 114.29161834716797, 0, isQueued = 1)
                dType.SetPTPJointParams(api, 100, 100, 100, 100, 100, 100, 100, 100, isQueued = 1)
                dType.SetPTPCommonParams(api, 50, 50, isQueued = 1)
                dType.SetARCCommonParams(api, 200, 200, isQueued = 1)
                dType.SetHOMECmdEx(api, 1, isQueued=1)
                dType.SetQueuedCmdStartExec(api)
                if stationNum == 1:
                    dType.SetPTPCmd(api, movj, 193.80259704589844, -91.76068115234375, 73.77569580078125, 64.2706069946289, isQueued=0)
                elif stationNum == 3:
                    dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=0) 

    def disconnect(self,stationNum):

        if stationNum == 1:
            api = self.api1
        elif stationNum == 2:
            api = self.api2
        elif stationNum == 3:
            api = self.api3
        dType.DisconnectDobot(api)
        
        print('연결 해제 완료')
        if self.plc.Close() == 0:
            if stationNum == 1:
                self.isConnected1 = False
            elif stationNum == 2:
                self.isConnected2 = False
            elif stationNum == 3:
                self.isConnected3 = False

    def GetPose(self,stationNum):
        if stationNum == 1:
            api = self.api1
        elif stationNum == 2:
            api = self.api2
        elif stationNum == 3:
            api = self.api3

        return [stationNum,
            dType.GetPose(api)[4],
            dType.GetPose(api)[5],
            dType.GetPose(api)[6],
            dType.GetPose(api)[7]]
            
    
    def Home(self,stationNum):
        if stationNum == 1:
            api = self.api1
        elif stationNum == 2:
            api = self.api2
        elif stationNum == 3:
            api = self.api3
        dType.SetHOMECmdEx(api, 1, isQueued=0)

    def robot1(self,_Device):

        movj = dType.PTPMode.PTPMOVJXYZMode
        movl =dType.PTPMode.PTPMOVLXYZMode

        api = self.api1
        if (self.state1 == dType.DobotConnect.DobotConnect_NoError):
            
            if _Device == 0:
                
                dType.SetPTPCmd(api, movl, 193.80259704589844, -91.76068115234375, 73.77569580078125, 64.2706069946289, isQueued=1) 
                dType.SetPTPCmd(api, movl, 193.80259704589844, -91.76068115234375, 14.255363464355469, 64.27061462402344, isQueued=1)
                dType.SetPTPCmd(api, movl, 193.80259704589844, -91.76068115234375, 14.255363464355469, 64.27061462402344, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movj, 193.80259704589844, -91.76068115234375, 73.77569580078125, 64.2706069946289, isQueued=1)
                dType.SetPTPCmd(api, movj, 5.596028757095337, -251.3144073486328, 60.001197814941406, -26.571914672851562, isQueued=1)
                dType.SetPTPCmd(api, movj, 5.596028757095337, -267.10247802734375, 40.00385284423828, -26.571914672851562, isQueued=1)
                dType.SetPTPCmd(api, movl, 5.596034049987793, -267.1034240722656, 15.62419891357422, -26.571914672851562, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movl, 5.596028757095337, -251.3144073486328, 60.001197814941406, -26.571914672851562, isQueued=1)          
                
            elif _Device == 1:   

                dType.SetPTPCmd(api, movl,193.80259704589844, -91.76068115234375, 60.77569580078125, 64.2706069946289, isQueued=1)    
                dType.SetPTPCmd(api, movl, 193.80259704589844, -91.76068115234375, 14.255363464355469, 64.27061462402344, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movj, 193.80259704589844, -91.76068115234375, 73.77569580078125, 64.2706069946289, isQueued=1)
                dType.SetPTPCmd(api, movj, 5.596028757095337, -251.3144073486328, 60.001197814941406, -26.571914672851562, isQueued=1)
                dType.SetPTPCmd(api, movl, 5.594710826873779, -288.54573974609375, 60.204517364501953, -26.571914672851562, isQueued=1)
                dType.SetPTPCmd(api, movl, 4.594710826873779, -288.54573974609375, 28.204517364501953, -26.571914672851562, isQueued=0)
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movl, 5.596028757095337, -251.3144073486328, 60.001197814941406, -26.571914672851562, isQueued=1)
                
            lastIndex = dType.SetPTPCmd(api, movj, 193.80259704589844, -91.76068115234375, 73.77569580078125, 64.2706069946289, isQueued=1)[0] 

            #Start to Execute Command Queue
            dType.SetQueuedCmdStartExec(api)

            while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                if not self.isStop1 and self.plc.GetDevice("M200")[1] == 1:
                    self.isStop1 = True
                    dType.SetQueuedCmdStopExec(api)
                elif self.isStop1 and self.plc.GetDevice("M200")[1] == 0:
                    self.isStop1 = False
                    dType.SetQueuedCmdStartExec(api)
                dType.dSleep(1000)

            self.run1 = False

            #Stop to Execute Command Queued
            # 
        #Disconnect Dobot
        # dType.DisconnectDobot(api)

    def robot2(self,_Device):
        
        movj = dType.PTPMode.PTPMOVJXYZMode
        movl = dType.PTPMode.PTPMOVLXYZMode

        api = self.api2
        if (self.state2 == dType.DobotConnect.DobotConnect_NoError):
            
            if _Device == 0:
                
                dType.SetPTPCmd(api, movl, 5.582981109619141, -203.95887756347656, 156.9364013671875, 0, isQueued=1) 
                dType.SetPTPCmd(api, movl, 5.582981109619141, -203.95887756347656, 156.9364013671875, 0, isQueued=1) 
                dType.SetPTPCmd(api, movl, 5.582981109619141, -252.56048583984375, 156.9364013671875, 0, isQueued=1)    
                dType.SetPTPCmd(api, movl, 5.582981109619141, -252.56048583984375, 150.9364013671875, 0, isQueued=1)    
                dType.SetWAITCmd(api, 500, isQueued=1)
                gripIndex1 = dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)[0]
                dType.SetWAITCmd(api, 2000, isQueued=1)
                dType.SetPTPCmd(api, movl, 5.582981109619141, -252.56048583984375, 156.9364013671875, 0, isQueued=1)    
                dType.SetPTPCmd(api, movj, 5.582981109619141, -196.79473876953125, 156.9364013671875, 0, isQueued=1)    
                dType.SetARCCmd(api, [75.353515625, -181.7982940673828, 152.9364013671875, 22.73912811279297], 
                                [193.84396362304688, 0.0574142932891846, 40.2476806640625, 89.40254211425781], isQueued=1 )
                dType.SetPTPCmd(api, movl, 193.84396362304688, 0.0574142932891846, 18.2476806640625, 89.40254211425781, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)
                gripIndex2 = dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)[0]
                dType.SetWAITCmd(api, 2000, isQueued=1)
                dType.SetPTPCmd(api, movl, 193.84396362304688, 0.0574142932891846, 50.2476806640625, 89.40254211425781, isQueued=1)
                # dType.SetPTPCmd(api, movj, -2.462111282348633, -189.3157958984375, 78.2039566040039, -94.13316345214844, isQueued=1)

            elif _Device == 1:

                
                dType.SetPTPCmd(api, movj, -0.7725620269775391, -204.97116088867188, 114.29161834716797, 0 , isQueued=1)
                dType.SetPTPCmd(api, movj, 59.901798248291016, -196.02142333984375, 114.29156494140625, 17.208480834960938 , isQueued=1)     
                dType.SetARCCmd(api, [138.06761169433594, -140.7730255126953, 53.834869384765625, 44.66006088256836], 
                                [186.84396362304688, -1.0574142932891846, 50.2476806640625, 89.40254211425781], isQueued=1 )
                dType.SetPTPCmd(api, movl, 186.84384155273438, -1.057413339614868, 14.12774658203125, 89.40254211425781, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                gripIndex1 = dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)[0]
                dType.SetWAITCmd(api, 2000, isQueued=1)
                dType.SetPTPCmd(api, movl, 186.84384155273438, -1.057413339614868, 70.12774658203125, 89.40254211425781, isQueued=1)
                dType.SetPTPCmd(api, movl, 290.84384155273438, -1.057413339614868, 70.12774658203125, 89.40254211425781, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                gripIndex2 = dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)[0]
                dType.SetWAITCmd(api, 2000, isQueued=1)
                dType.SetPTPCmd(api, movl, 186.84384155273438, -1.057413339614868, 70.12774658203125, 89.40254211425781, isQueued=1)
                # dType.SetPTPCmd(api, movj, -2.462111282348633, -189.3157958984375, 78.2039566040039, -94.13316345214844, isQueued=1)

            lastIndex = dType.SetPTPCmd(api, movj, -0.7725620269775391, -204.97116088867188, 114.29161834716797, 0 , isQueued=1)[0] 

            #Start to Execute Command Queue
            dType.SetQueuedCmdStartExec(api)

            while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                if not self.isStop2 and self.plc.GetDevice("M201")[1] == 1:
                    self.isStop2 = True
                    dType.SetQueuedCmdStopExec(api)
                elif self.isStop2 and self.plc.GetDevice("M201")[1] == 0:
                    self.isStop2 = False
                    dType.SetQueuedCmdStartExec(api)

                if dType.GetQueuedCmdCurrentIndex(api)[0] == gripIndex1:
                    self.plc.SetDevice("M203",1)
                elif dType.GetQueuedCmdCurrentIndex(api)[0] == gripIndex2:
                    self.plc.SetDevice("M203",0)
                    self.plc.SetDevice("M205",1)
                    time.sleep(0.01)
                    self.plc.SetDevice("M205",0)


                dType.dSleep(1000)


            self.run2 = False

    def robot3(self,_Device):
        
        movj = dType.PTPMode.PTPMOVJXYZMode
        movl =dType.PTPMode.PTPMOVLXYZMode

        api = self.api3
        if (self.state3 == dType.DobotConnect.DobotConnect_NoError):

            # if _Device == 0:

            #     dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
            #     dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
            #     dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1)
            #     dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1) 
            #     dType.SetWAITCmd(api, 500, isQueued=1)
            #     dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
            #     dType.SetWAITCmd(api, 500, isQueued=1)
            #     dType.SetPTPCmd(api, movl, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1)    
            #     dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
            #                     [72.70623779296875, 250.2193603515625, 134.89944458007812, 183.05303955078125], isQueued=1 )
            #     dType.SetPTPCmd(api, movl, 72.71221160888672, 250.23992919921875, 52.801544189453125, 181.3735809326172, isQueued=1)
            #     dType.SetWAITCmd(api, 500, isQueued=1)
            #     dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
            #     dType.SetWAITCmd(api, 500, isQueued=1)
            #     dType.SetPTPCmd(api, movl, 72.71221160888672, 250.23992919921875, 134.89944458007812, 181.3735809326172, isQueued=1)
            #     dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
            #                     [259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344], isQueued=1 )
        
            if _Device == 1:

                dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
                dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
                dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1)
                dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1)   
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movl, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1)    
                dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
                                [72.70623779296875, 250.2193603515625, 134.89944458007812, 183.05303955078125], isQueued=1 )
                dType.SetPTPCmd(api, movl, 72.71221160888672, 250.23992919921875, 52.801544189453125, 181.3735809326172, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movl, 72.71221160888672, 250.23992919921875, 134.89944458007812, 181.3735809326172, isQueued=1)
                dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
                                [259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344], isQueued=1 )

            elif _Device == 2:

                dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
                dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
                dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1)
                dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1)  
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movl, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1)    
                dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
                                [17.388887405395508, 247.11630249023438, 134.89944458007812, 183.0537872314453], isQueued=1 )
                dType.SetPTPCmd(api, movl, 17.388887405395508, 247.11630249023438, 52.801544189453125, 183.0537872314453, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movl, 17.388887405395508, 247.11630249023438, 134.89944458007812, 183.0537872314453, isQueued=1)
                dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
                                [259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344], isQueued=1 )

            elif _Device == 3:

                dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
                dType.SetPTPCmd(api, movj, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1) 
                dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1) 
                dType.SetPTPCmd(api, movl, 259.43218994140625, 23.712913513183594, 20.419631958007812, 91.50889587402344, isQueued=1)    
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)  # 흡착 ON
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movl, 259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344, isQueued=1)    
                dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
                              [-37.93241500854492, 248.44430541992188, 134.89944458007812, 183.0537872314453], isQueued=1 )
                dType.SetPTPCmd(api, movl, -37.93241500854492, 248.44430541992188, 52.801544189453125, 183.0537872314453, isQueued=1)
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetEndEffectorSuctionCup(api, 1, 0, isQueued=1)  # 흡착 OFF
                dType.SetWAITCmd(api, 500, isQueued=1)
                dType.SetPTPCmd(api, movl, -37.93241500854492, 248.44430541992188, 134.89944458007812, 183.0537872314453, isQueued=1)
                dType.SetARCCmd(api, [229.1664581298828, 113.18804168701172, 123.88801574707031, 112.61143493652344], 
                                [259.43060302734375, 23.712770462036133, 81.5190658569336, 91.50889587402344], isQueued=1 )

                
            lastIndex = dType.SetPTPCmd(api, movj, 259.4306335449219, 23.712833404541016, 81.51910400390625, 91.5084228515625 , isQueued=1)[0] 

            #Start to Execute Command Queue
            dType.SetQueuedCmdStartExec(api)

            while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                if not self.isStop3 and self.plc.GetDevice("M202")[1] == 1:
                    self.isStop3 = True
                    dType.SetQueuedCmdStopExec(api)
                elif self.isStop3 and self.plc.GetDevice("M202")[1] == 0:
                    self.isStop3 = False
                    dType.SetQueuedCmdStartExec(api)
                dType.dSleep(1000)

            self.run3 = False