import DobotControl3 as dc
import time
import socket
import msvcrt
import struct

test = dc.Dobot()

test.connect(2,11)

HOST = '127.0.0.1'
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # 루프 바깥에서 딱 1번 연결

    while test.isConnected2:

        pose = test.GetPose(2)
        print(pose)
        data = struct.pack('Bffff', *pose)
        s.sendall(data)

        run = test.plc.GetDevice("X201")[1]
        device = test.plc.GetDevice("D3001")[1]

        if run == 1:

            test.run2 = True
            test.robot2(device)
        
            if not test.run2:
                test.plc.SetDevice("Y201",1)
                time.sleep(0.05)
                test.plc.SetDevice("Y201",0)

                if test.plc.GetDevice("D3001")[1] == 1:

                    test.plc.SetDevice("Y205",1)
                    time.sleep(0.1)
                    test.plc.SetDevice("Y205",0)

        if msvcrt.kbhit():  # 키가 눌렸는지 확인
            key = msvcrt.getch()  # 눌린 키를 가져옴
            if key == b'q':
                test.disconnect(2)  # 예: 'q' 키가 눌렸다면
                print('연결 해제 성공')
                break
            elif key == b'h':
                test.Home(2)

    time.sleep(0.05)