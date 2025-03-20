import DobotControl as dc
import win32com.client
import time

test = dc.Dobot()
plc = win32com.client.Dispatch("ActUtlType.ActUtlType")

plc.ActLogicalStationNumber = 1
isConnected = False

result = plc.Open()

if result == 0:
    isConnected = True
    print('연결 성공')
    
    while isConnected:
  
        run = plc.GetDevice("M0")

        print(run)
        if run[1] == 1:

            num = 3
            test.demotest(num)
                
            plc.SetDevice("M0",0)

        time.sleep(1)


else:
    print(f'연결 실패 (에러코드 {result})')   
