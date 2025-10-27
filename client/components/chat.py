from datetime import datetime, timezone
from colorama import Fore, Style, init
from Crypto.Cipher import AES
from dotenv import load_dotenv
import os
import sys
import asyncio
import websockets
from pathlib import Path
import json
import base64
import time

init(autoreset=True)
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / '.env')

AES_KEY = (os.getenv("AES_KEY")).encode('utf-8')
iv = (os.getenv("iv")).encode('utf-8')

def clear_lines(n=1):
    """Clear the previous `n` lines from the terminal output."""
    for _ in range(n):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

async def chat(userId, recipient):
    uri = (f'ws://localhost:8080')
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        async with websockets.connect(uri) as websocket:
            print(Fore.GREEN + (f"Welcome {userId}! CBJ-CHAT started at {date}. Type 'exit' to quit."))
            print(Fore.YELLOW + (f"WARNING: Dont send any sensitive chat at testing server!"))

            async def receive_messages():
                try:
                    async for message in websocket:
                        sys.stdout.write("\033[2K\r")

                        # Decrypt the message
                        encrypted_msg = base64.b64decode(message)
                        objDec = AES.new(AES_KEY, AES.MODE_CBC, iv)
                        decrypted_msg = objDec.decrypt(encrypted_msg)

                        # Remove padding
                        padding_length = decrypted_msg[-1]
                        decrypted_msg = decrypted_msg[:-padding_length]
                        message = decrypted_msg.decode('utf-8')
                        
                            
                        if recipient == 'devtools':
                            print("\r", end="")
                            print((f"{Fore.LIGHTCYAN_EX}{date} ({json.loads(message)['userId']} to {json.loads(message)['recipient']})") + (f"{Fore.WHITE}: {json.loads(message)['message']}"))
                            print(">>: ", end="", flush=True)
                        elif json.loads(message)['recipient'] == recipient or json.loads(message)['recipient'] == userId: # or json.loads(message)['recipient'] == 'devtools': (Send to all user settings. Default settings = Disabled)
                            print("\r", end="")
                            print((f"{Fore.LIGHTCYAN_EX}{date} ({json.loads(message)['userId']} to {json.loads(message)['recipient']})") + (f"{Fore.WHITE}: {json.loads(message)['message']}"))
                            print(">>: ", end="", flush=True)
                        else: 
                            print(">>: ", end="", flush=True)
                            pass

                except websockets.ConnectionClosed:
                    print(Fore.RED + "Connection closed.")
                    return

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
                    break

                # COMMANDS 
                if userId == 'DEV' and user_input == ':info'.lower():
                    print((Fore.GREEN + ".:CHAT IN TERMINAL:.") + "\nYou are currently using DEV account")
                if userId == 'DEV':
                    print(f'{Fore.YELLOW}DEFAULT: Devtools users cannot send chat to anyone. They are can receive message from everyone. \nEnable receive dev message for all client on chat.py file lines 52 to') # Friendly warning
                if user_input.startswith('reply:'.lower()):
                    ReplyUser = user_input.split("reply:", 1)[1].strip()
                    if not ReplyUser:
                        print(f'{Fore.RED}ReplyUser cannot be null!')
                    else:
                        print(f'{Fore.GREEN}INFO: Reply mode to {ReplyUser} user')
                        recipient = ReplyUser
                        continue

                msg = {
                    "userId": userId,
                    "message": user_input,
                    "recipient": recipient,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                

                # Encrypt the message
                unencrypted_msg = json.dumps(msg).encode('utf-8')

                # Padding
                block_size = 16
                padding_length = block_size - (len(unencrypted_msg) % block_size)
                unencrypted_msg += bytes([padding_length]) * padding_length

                # Encryption
                objMsg = AES.new(AES_KEY, AES.MODE_CBC, iv)
                AES_msg = objMsg.encrypt(unencrypted_msg)  
                encrypted_msg = base64.b64encode(AES_msg)

                await websocket.send(encrypted_msg)
                clear_lines(1)
                print((f"{Fore.LIGHTCYAN_EX}{date} ({msg['userId']} to {msg['recipient']})") + (f"{Fore.WHITE}: {msg['message']}"))


    except ConnectionRefusedError:
        print(Fore.RED + "Server currently offline.")


