import asyncio
import DobotControl2 as dc
import win32com.client
import time

class AsyncTest():
    def __init__(self):
        self.plc = win32com.client.Dispatch("ActUtlType.ActUtlType")
        self.isConnected = False
        self.ActLogicalStationNum = None
        self.stop_flag = 0  # 비상 정지 플래그
        self.test = dc.Dobot()

    def Connect(self, _num):
        self.ActLogicalStationNum = _num
        result = self.plc.Open()
        if result == 0:
            self.isConnected = True
        return result

    async def DobotAsync(self):
        while self.isConnected:
            run = self.plc.GetDevice("M100")
            print(run)

            if run[1] == 1:
                num = 3

                # 로봇 동작과 동시에 비상정지 감지를 백그라운드 태스크로 실행
                emergency_task = asyncio.create_task(self.Emergency())
                dobot_task = asyncio.create_task(asyncio.to_thread(self.test.demotest, num))

                # 두 개의 태스크 중 하나가 끝날 때까지 대기
                await asyncio.wait(
                    [dobot_task, emergency_task], return_when=asyncio.FIRST_COMPLETED
                )

                # 비상정지가 감지된 경우, 로봇 동작 취소
                while self.stop_flag == 1:
                    print("[E-STOP] 비상정지 감지! 로봇 정지 중...")
                    # dobot_task.cancel()  # 실행 중이던 로봇 동작 취소
                    self.test.Estop()  # Dobot 정지

                # 비상정지가 아니면 정상 동작 후 Y200 신호 전송

                self.plc.SetDevice("Y200", 1)
                time.sleep(0.01)
                self.plc.SetDevice("Y200", 0)

            await asyncio.sleep(1)

    async def Emergency(self):
        """ PLC에서 M200 신호 감지 시, 즉시 비상 정지 """
        while self.isConnected:
            print("비상정지 대기중")

            self.stop = self.plc.GetDevice("M200")
            print(self.stop)

            if self.stop[1] == 1:
                self.stop_flag = 1  # 비상 정지 플래그 설정
                print("[E-STOP] 비상 정지 신호 감지!")
                return  # 비상정지 감지 즉시 종료
            
            elif self.stop[1] == 0:
                self.stop_flag = 0

            await asyncio.sleep(0.1)  # 빠른 감지를 위해 주기 단축


