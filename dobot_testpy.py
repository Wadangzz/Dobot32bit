import DobotControl as dc
import win32com.client
import time

plc = win32com.client.Dispatch("ActUtlType.ActUtlType")

plc.ActLogicalStationNumber = 1
isConnected = False

result = plc.Open()

if result == 0:
    isConnected = True
    print('연결 성공')
    
    while isConnected:
  
        run = plc.GetDevice("M100")

        print(run[1])
        if run[1] == 1:
             print(run)
            # # test.test()
            
            # plc.SetDivice("M100",0)
        time.sleep(1)


else:
    print(f'연결 실패 (에러코드 {result})')   


# while True:
  
#     if row[1] == 1:

#         test = dc.DobotTest()
#         test.test()
#         cursor.execute("SELECT address, value FROM DigitalTags WHERE address = ?", ('M100',))
        
#     time.sleep(1)