import DobotControl3 as dc
import win32com.client
import time

test = dc.Dobot()
plc = win32com.client.Dispatch("ActUtlType.ActUtlType")

plc.ActLogicalStationNumber = 6
isConnected = False

result = plc.Open()

if result == 0:
    isConnected = True
    print('연결 성공')
    test.connect(3)

    while isConnected:
  
        run = plc.GetDevice("M100")[1]
        device = plc.GetDevice("D100")[1]
        # isStop = plc.GetDevice("M200")[1]

        print(run,device)

        if run == 1:

            if not test.run: 
                test.run = True
                test.demotest(device)
            
                if not test.run:
                    plc.SetDevice("Y200",1)
                    time.sleep(0.1)
                    plc.SetDevice("Y200",0)

        time.sleep(1)

else:
    print(f'연결 실패 (에러코드 {result})')   
