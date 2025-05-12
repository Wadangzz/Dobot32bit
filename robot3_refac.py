import DobotControl as dc
import time
import socket
import struct
import msvcrt
import threading

HOST = '127.0.0.1'
PORT = 8000
stop_thread = False  # 종료 시그널용

# 소켓을 통해 포즈를 전송하는 함수
# 스레드 분리하여 실행
def send_pose_loop(sock):

    while test.bot[3]["isConnected"] and not stop_thread:
        # test.GetPose(3)로 로봇 3의 포즈를 가져옴   
        pose = test.GetPose(3)
        print("pose:", pose)

        # PLC_NModbus C# Server에 Joint Angle 전송
        try:
            data = struct.pack('<Bffff', pose[0] ,*pose[1:5])
            sock.sendall(data)
        except Exception as e:
            print(f"데이터 전송 오류: {e}")
            break
        if not test.bot[3]["isConnected"]:
            break

        time.sleep(0.001)
\
# Dobot 객체 생성 및 연결
test = dc.Dobot()
test.connect(3,12)

# 8000번 포트로 소켓 서버를 열고, 클라이언트가 연결될 때까지 대기
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # 루프 바깥에서 딱 1번 연결
    
    # 소켓을 통해 포즈를 전송하는 스레드를 시작
    pose_thread = threading.Thread(target=send_pose_loop, args=(s,))
    pose_thread.start()

    # 로봇 3이 연결되있는 경우 루프 동작
    # PLC에서 X202, X219, D3002의 값을 읽어옴
    while test.bot[3]["isConnected"]:

        run = test.plc.GetDevice("X202")[1]
        homing = test.plc.GetDevice("X219")[1]
        device = test.plc.GetDevice("D3002")[1]
        
        # run이 1이면 로봇을 동작시킴
        if run == 1:

            test.bot[3]["run"] = True
            test.robot(3,device)

            # 로봇 run이 0이면 로봇을 정지시킴
            if not test.bot[3]["run"]:
                test.plc.SetDevice("Y202",1)
                time.sleep(0.1)
                test.plc.SetDevice("Y202",0)

        # homing이 1이면 로봇을 홈으로 이동
        if homing == 1:
            test.Home(3)

        if msvcrt.kbhit():  # 키가 눌렸는지 확인
            key = msvcrt.getch()  # 눌린 키를 가져옴
            if key == b'q': # 'q' 키가 눌렸다면
                stop_thread = True  # 스레드 종료 시그널  
                test.disconnect(3)  # 로봇 연결 해제  
                pose_thread.join() # 스레드 종료 대기
                break
            elif key == b'h':
                test.Home(3)

        time.sleep(0.05)
    

