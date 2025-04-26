import DobotControl3 as dc
import time
import socket
import msvcrt
import struct
import threading

HOST = '127.0.0.1'
PORT = 8000
stop_thread = False  # 종료 시그널용

def send_pose_loop(sock):

    while test.isConnected2 and not stop_thread:
        pose = test.GetPose(2)
        print("pose:", pose)

        try:
            data = struct.pack('<Bffff', pose[0] ,*pose[1:5])
            sock.sendall(data)
        except Exception as e:
            print(f"데이터 전송 오류: {e}")
            break
        if not test.isConnected2:
            break

        time.sleep(0.001)

test = dc.Dobot()
test.connect(2,11)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # 루프 바깥에서 딱 1번 연결

    pose_thread = threading.Thread(target=send_pose_loop, args=(s,))
    pose_thread.start()

    while test.isConnected2:

        run = test.plc.GetDevice("X201")[1]
        homing = test.plc.GetDevice("X218")[1]
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

        if homing == 1:
            test.Home(2)

        if msvcrt.kbhit():  # 키가 눌렸는지 확인
            key = msvcrt.getch()  # 눌린 키를 가져옴
            if key == b'q':
                stop_thread = True
                test.disconnect(2)  # 예: 'q' 키가 눌렸다면
                pose_thread.join()
                break
            elif key == b'h':
                test.Home(2)

        time.sleep(0.05)