from datetime import datetime
import sys
import asyncio
import websockets

userId = '001'

def clear_lines(n = int):
    for _ in range(n):
        sys.stdout.write("\033[F")  
        sys.stdout.write("\033[K")

async def chat():
    uri = 'ws://localhost:8080'
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"CBJ-CHAT started at {date}. Type 'exit' to quit.")

    async with websockets.connect(uri) as websocket:
        while True:
            user_input = input(">>: ")
            clear_lines(1)
            if user_input.lower() == 'exit' or user_input.lower() == '^c':
                print("CBJ-CHAT ended. Goodbye!")
                await websocket.close()
                break
            if not user_input.strip():
                clear_lines(2)
                continue

            msg = f"[{datetime.now().strftime('%H:%M:%S')}] {userId}: {user_input}"
            await websocket.send(msg)
            print(msg)

            response = await websocket.recv()

            print(response)

asyncio.run(chat())