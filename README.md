# 🤖 Dobot32bit

## 📘 프로젝트 개요

**Dobot32bit**는 Python 기반으로 Mitsubishi PLC와 통신하여,  
**이벤트 트리거 기반으로 Dobot Magician 로봇 3대를 제어**하고,  
각 로봇의 실시간 포즈(joint angle)를 **PLC_NModbus 서버에 소켓으로 전송**하는 프로젝트입니다.

---

## 🔧 주요 기능

- **PLC 통신 제어**  
  ActUtlType으로 Mitsubishi PLC와 연결하여 각 Dobot의 동작 조건을 판단하고 제어합니다.

- **Dobot 3대 독립 제어**  
  `robot1_refac.py`, `robot2_refac.py`, `robot3_refac.py`는 각각 Dobot 1, 2, 3의 동작을 수행하며  
  장착된 장치(흡착기, 그리퍼)를 활용한 pick & place 작업을 수행합니다.

- **소켓 통신 기반 포즈 전송**  
  각 Dobot의 관절 각도(joint1 ~ joint4)를 실시간으로 소켓을 통해 전송(`struct.pack('<Bffff', ...)`)

- **동시성 제어**  
  각 로봇은 별도 스레드로 동작하면서도 PLC 상태에 따라 정지/재시작이 가능합니다.

---

## 🗂️ 프로젝트 구조

| 파일 | 설명 |
|------|------|
| `DobotDllType.py` | Dobot SDK DLL 구조 정의 (ctypes 기반 구조체 및 API 래핑) |
| `DobotControl.py` | 로봇 1~3의 연결, 동작 처리, 포즈 수집 및 PLC 통신 담당 |
| `robot1_refac.py` | Dobot 1번 제어 및 포즈 전송, 이벤트: X200, Y200 |
| `robot2_refac.py` | Dobot 2번 제어 및 포즈 전송, 이벤트: X201, Y201, M203, M205 |
| `robot3_refac.py` | Dobot 3번 제어 및 포즈 전송, 이벤트: X202, Y202 |

---

## 🔄 시스템 동작 흐름

```plaintext
[PLC X20X 입력 감지] → [Dobot 연결] → [흡착/이동 등 작업 수행]
                             ↳ 작업 종료 시 Y20X 출력
                             ↳ 동작 중 실시간 Pose 정보 TCP 전송 (127.0.0.1:8000)

[PLC 정지 조건 발생 (M20X)] → 로봇 동작 일시정지
                         ↳ 해제되면 재개

[긴급 정지 (X21A)] → 완전 비상정지
```
