from datetime import datetime
from aioconsole import ainput
from colorama import Fore, Style, init
init(autoreset=True)
import sys
import asyncio
import websockets

userId = '001'

def clear_lines(n = int):
    for _ in range(n):
        sys.stdout.write("\033[F")  
        sys.stdout.write("\033[K")

async def chat():
    sessionId = '8080'
    uri = 'ws://localhost:8080'
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(Fore.GREEN + (f"CBJ-CHAT started at {date} with session id {sessionId}. Type 'exit' to quit."))

    async with websockets.connect(uri) as websocket:

        async def receive_messages():
            try:
                async for message in websocket:
                    sys.stdout.write("\033[K")
                    sys.stdout.write("\033[F") 
                    print("")
                    print(message)
                    print(">>: ", end="", flush=True)
            except websockets.ConnectionClosed:
                print(Fore.RED + "Connection closed.")

        asyncio.create_task(receive_messages())

        while True:
            user_input = await ainput(">>: ")
            clear_lines(1)
            if user_input.lower() == 'exit' or user_input.lower() == '^C':
                print("CBJ-CHAT ended. Goodbye!")
                await websocket.close()
                break
            if not user_input.strip():
                clear_lines(2)
                continue

            msg = f"[{datetime.now().strftime('%H:%M:%S')}] {userId}: {user_input}"
            await websocket.send(msg)
            print(msg)


asyncio.run(chat())