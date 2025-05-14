# 🤖 Dobot32bit

## 📘 프로젝트 개요

**Dobot32bit**는 Python 기반으로 Mitsubishi PLC와 통신하여,  
PLC 신호를 통해 **Dobot Magician 로봇 3대를 제어**하고,  
각 로봇의 실시간 포즈(joint angle)를 **PLC_NModbus 서버에 소켓으로 전송**하는 프로젝트입니다.

Dobot SDK와 Mitsubishi MX Component ActUtlType.dll를 import 하려면
Python 32bit 환경을 구축해야 합니다.(사용한 Python version 3.9)

```
set CONDA_FORCE_32BIT = 1
conda create -n "가상환경 이름" python=3.9
```

32bit 가상환경 설정 후 pywin32 package 설치해서
ActUtlType.dll을 import 합니다.
```
pip install pywin32
plc = win32com.client.Dispatch("ActUtlType.ActUtlType")
```
---

## 🔧 주요 기능

- **PLC 통신 제어**  
  ActUtlType으로 Mitsubishi PLC와 연결하여 각 Dobot의 동작 조건을 판단하고 제어합니다.

- **Dobot 3대 독립 제어**  
  `robot1.py`, `robot2.py`, `robot3.py`는 각각 Dobot 1, 2, 3의 동작을 수행하며  
  병렬 동작이 가능하고 장착된 장치(흡착기, 그리퍼)를 활용한 pick & place 작업을 수행합니다.

- **소켓 통신 기반 포즈 전송**  
  각 Dobot의 관절 각도(joint1 ~ joint4)를 실시간으로 소켓을 통해 전송(`struct.pack('<Bffff', ...)`)

---

## 🗂️ 프로젝트 구조

| 파일 | 설명 |
|------|------|
| `DobotDllType.py` | Dobot SDK DLL 구조 정의 (ctypes 기반 구조체 및 API 래핑) |
| `DobotControl.py` | 로봇 1~3의 연결, 동작 처리, 포즈 수집 및 PLC 통신 담당 |
| `robot1.py` | Dobot 1번 제어 및 포즈 전송, 이벤트: X200, Y200 |
| `robot2.py` | Dobot 2번 제어 및 포즈 전송, 이벤트: X201, Y201, M203, M205 |
| `robot3.py` | Dobot 3번 제어 및 포즈 전송, 이벤트: X202, Y202 |

---

## 🔄 시스템 동작 흐름

| **조건 / 이벤트**       | **동작 내용** |
|-------------------------|----------------|
| `X20@` 입력 감지         | PLC에서 로봇 동작 요청 수신 → Dobot 연결 및 경로 실행 |
| 작업 수행 중            | 물체 흡착 → 이동 → 배치 수행<br>실시간 Pose 정보 TCP 전송 (`127.0.0.1:8000`) |
| 작업 완료               | `Y20X` 출력 → Master PLC에 작업 완료 신호 전달 |
| `M20@` ON (정지 조건)    | 로봇 동작 일시정지 (`SetQueuedCmdStopExec`) |
| `M20@` OFF              | 일시정지 해제 후 재시작 (`SetQueuedCmdStartExec`) |
| `X21A` ON (비상 정지)    | 모든 명령 큐 클리어 (`SetQueuedCmdClear`) + 흡착 해제<br>`M205` 신호 전송 (2번 로봇 그리퍼 리셋) |

---

## 🐞 Trouble Shooting

### 🧩 1. C# 소켓 수신 오류 (Endian 정렬 문제)

**문제**  
Python에서 `struct.pack('Bffff', ...)`로 로봇 ID와 joint1~4 값을 17 byte로 패킹해 전송했지만,  
C# 서버측에서 **데이터 순서를 정확히 해석하지 못하고 변질**되는 문제가 발생

**해결방법**  
패킹 시 **리틀엔디안(Little Endian)을 명시적으로 지정**하기 위해  
`struct.pack('<Bffff', ...)` 형태로 수정하여,  **모든 float 값이 리틀엔디안 순서로 정렬되도록 처리**('<' 추가)

**결과**  
C# 서버측에서 **로봇 ID부터 각 관절 값까지 순서대로 정확히 수신 및 해석**할 수 있게 되어,  
데이터 손실 없이 실시간 포즈 연동이 가능해졌습니다.

---

## 💡 To Me

Dobot32bit 프로젝트를 통해 **PLC 신호 기반의 로봇 제어 시스템을 스스로 설계하고 구현**하는 과정을 경험했습니다.  
Dobot 3대를 개별 스크립트로 병렬 실행하면서, **여러 대의 로봇이 독립적으로 병렬 동작하는 구조**를 직접 구성했고,  
**로봇–PLC–상위 서버 간의 실시간 통신 흐름**을 이해할 수 있었습니다.

특히 서로 다른 환경(Python–C#) 간의 **데이터 포맷 정렬 문제(Endian)**를 해결하며,  
**하드웨어 제어에서 발생할 수 있는 통신 이슈를 실제로 경험하고 디버깅하는 역량**을 키울 수 있었습니다.

단순 제어를 넘어서 **로봇 제어, PLC 통신, 실시간 데이터 연동이 통합된 구조를 직접 설계하고 운영**한 경험은  
향후 다양한 자동화 시스템 개발에 **직접 적용 가능한 실전 경험**이 되었습니다.
