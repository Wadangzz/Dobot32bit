import asynctest as asy
import asyncio

test = asy.AsyncTest()

async def process():
    print(test.Connect(6))

    while test.isConnected:  # PLC 연결이 유지되는 동안 반복 실행
        # Dobot 동작과 비상정지 감지를 동시에 실행
        await asyncio.wait([
            asyncio.create_task(test.DobotAsync()),
            asyncio.create_task(test.Emergency()) 
        ])

    await asyncio.sleep(0.01)  # 1초마다 비상정지 상태 확인

asyncio.run(process())
