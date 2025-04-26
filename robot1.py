import DobotControl3 as dc
import time
import socket
import struct
import msvcrt
import threading

HOST = '127.0.0.1'
PORT = 8000
stop_thread = False  # 종료 시그널용

def send_pose_loop(sock):

    while test.isConnected1 and not stop_thread:
        pose = test.GetPose(1)
        print("pose:", pose)

        try:
            data = struct.pack('<Bffff', pose[0] ,*pose[1:5])
            sock.sendall(data)
        except Exception as e:
            print(f"데이터 전송 오류: {e}")
            break
        if not test.isConnected1:
            break

        time.sleep(0.001)

test = dc.Dobot()
test.connect(1,10)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # 루프 바깥에서 딱 1번 연결

    pose_thread = threading.Thread(target=send_pose_loop, args=(s,))
    pose_thread.start()

    while test.isConnected1:

        run = test.plc.GetDevice("X200")[1]
        homing = test.plc.GetDevice("X217")[1]
        device = test.plc.GetDevice("D3000")[1]

        if run == 1:

            test.run1 = True
            test.robot1(device)
        
            if not test.run1:
                test.plc.SetDevice("Y200",1)
                time.sleep(0.1)
                test.plc.SetDevice("Y200",0)
                
        if homing == 1:
            test.Home(1)

        if msvcrt.kbhit():  # 키가 눌렸는지 확인
            key = msvcrt.getch()  # 눌린 키를 가져옴
            if key == b'q':
                stop_thread = True
                test.disconnect(1)  # 'q' 키가 눌렸다면
                pose_thread.join()
                break
            elif key == b'h':
                test.Home(1)

        time.sleep(0.05)