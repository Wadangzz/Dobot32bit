import asyncio
import DobotControl2 as dc
import win32com.client
import time


class AsyncTest():

    def __init__(self):
        
        self.plc = win32com.client.Dispatch("ActUtlType.ActUtlType")
        self.isConnected = False
        self.ActLogicalStationNum = None
        self.stop = None
        self.test = dc.Dobot()


    def Connect(self,_num):

        self.ActLogicalStationNum = _num
        result = self.plc.Open()
        if result == 0:
            self.isConnected = True
        return result

    async def DobotAsync(self):
        
        while self.isConnected:
            
            run = self.plc.GetDevice("M100")
            if run[1] == 1:

                num = 3
                task = asyncio.to_thread(self.test.demotest, num)
                await task
                    
                self.plc.SetDevice("Y200",1)
                time.sleep(0.01)
                self.plc.SetDevice("Y200",0)

            await asyncio.sleep(0.01)

    async def Emergency(self):

        while self.isConnected:
            
            self.stop = self.plc.GetDevice("M200")
            if self.stop == 0:
                print("비상정지 대기중")
            elif self.stop[1] == 1:
                self.test.Estop() # 비상 정지 플래그 설정
                print("[E-STOP] 비상 정지 신호 감지!")

            await asyncio.sleep(0.01)

    
        
