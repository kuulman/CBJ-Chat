from datetime import datetime
import os
from colorama import Fore, Style, init
from Crypto.Cipher import AES
from dotenv import load_dotenv
init(autoreset=True)
import sys
import asyncio
import websockets
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / '.env')

userId = '001'

def clear_lines(n=1):
    """Clear the previous `n` lines from the terminal output."""
    for _ in range(n):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

async def chat(sessionID):
    uri = (f'ws://localhost:{sessionID}')
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    try:
        async with websockets.connect(uri) as websocket:
            print(Fore.GREEN + (f"CBJ-CHAT started at {date} with session id {sessionID}. Type 'exit' to quit."))

            async def receive_messages():
                try:
                    async for message in websocket:
                        sys.stdout.write("\033[K")
                        sys.stdout.write("\033[F") 
                        print(message)
                        print(">>: ", end="", flush=True)
                except websockets.ConnectionClosed:
                    print(Fore.RED + "Connection closed.")

            asyncio.create_task(receive_messages())

            # Provide an async-compatible input fallback so we don't depend on
            # the external `aioconsole` package. This uses asyncio.to_thread
            # to run the blocking `input()` in a thread.
            async def ainput(prompt=""):
                return await asyncio.to_thread(input, prompt)

            while True:
                try:
                    user_input = await ainput(">>: ")
                    if user_input.lower() == 'exit':
                        print("CBJ-CHAT ended. Goodbye!")
                        await websocket.close()
                        return
                    if not user_input.strip():
                        clear_lines()
                        continue

                except KeyboardInterrupt:
                    print("\nExiting chat.")
                    await websocket.close()
                    return

                msg = f"[{datetime.now().strftime('%H:%M:%S')}] {userId}: {user_input}"

                # Encrypt the message
                AES_KEY = (os.getenv("AES_KEY")).encode('utf-8')
                iv = (os.getenv("iv")).encode('utf-8')
                unencrypted_msg = msg.encode('utf-8')
                objMsg = AES.new(AES_KEY, AES.MODE_CBC, iv)
                encrypted_msg = objMsg.encrypt(unencrypted_msg.ljust(32))  # Padding for block size

                await websocket.send(encrypted_msg)
                clear_lines(1)
                print(msg)

    except ConnectionRefusedError:
        print(Fore.RED + "Server currently offline.")
