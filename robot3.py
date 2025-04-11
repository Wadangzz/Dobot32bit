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

    while test.isConnected3 and not stop_thread:
        pose = test.GetPose(3)
        print("pose:", pose)

        try:
            data = struct.pack('<Bffff', pose[0] ,*pose[1:5])
            sock.sendall(data)
        except Exception as e:
            print(f"데이터 전송 오류: {e}")
            break

        time.sleep(0.001)

test = dc.Dobot()
test.connect(3,12)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # 루프 바깥에서 딱 1번 연결

    pose_thread = threading.Thread(target=send_pose_loop, args=(s,))
    pose_thread.start()

    while test.isConnected3:

        run = test.plc.GetDevice("X202")[1]
        homing = test.plc.GetDevice("X219")[1]
        device = test.plc.GetDevice("D3002")[1]
        

        if run == 1:

            test.run3 = True
            test.robot3(device)
        
            if not test.run3:
                test.plc.SetDevice("Y202",1)
                time.sleep(0.1)
                test.plc.SetDevice("Y202",0)

        if homing == 1:
            test.Home(3)

        if msvcrt.kbhit():  # 키가 눌렸는지 확인
            key = msvcrt.getch()  # 눌린 키를 가져옴
            if key == b'q':
                stop_thread = True
                test.disconnect(3)  # 예: 'q' 키가 눌렸다면
                pose_thread.join()
                break
            elif key == b'h':
                test.Home(3)

        time.sleep(0.05)
    

