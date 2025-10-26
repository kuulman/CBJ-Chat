from components.chat import chat
import asyncio
import sys
import time
import traceback


def prompt_session():
    try:
        return input("Enter user ID to join (e.g., user): ").strip()
    except EOFError:
        # EOF means no more input (e.g., user pressed Ctrl-D). Exit the loop.
        print("\nExiting.")
        return None

def prompt_session2():
    try:
        return input("Message to: ").strip()

    except EOFError:
        # EOF means no more input (e.g., user pressed Ctrl-D). Exit the loop.
        print("\nExiting.")
        return None
    
def devtools():
    try:
        return input("Devtools access key: ")
    except:
        # EOF means no more input (e.g., user pressed Ctrl-D). Exit the loop.
        print("\nExiting.")
        return None

while True:
    try:
        input_session = prompt_session()
    except KeyboardInterrupt:
        print("\nExiting.")
        break

    if input_session is None or input_session.strip() == "":
        continue

    try:
        input_session2 = prompt_session2()
    except KeyboardInterrupt:
        print("\nExiting.")
        break

    if input_session2 is None or input_session2.strip() == "":
        continue

    try:
        if input_session2 == 'devtools':   
            input_dev = devtools()
            if input_dev == 'devtools':
                input_session = 'DEV'
            else:
                print("You're not developer!")
                continue
        else:
            pass
    except KeyboardInterrupt:
        print("\nExiting.")
        break

    try:
        asyncio.run(chat(input_session, input_session2))
    except ConnectionRefusedError:
        # chat() already prints a friendly message when server is offline,
        # but handle residual ConnectionRefusedError here as well.
        time.sleep(0.1)
        continue
    except Exception:
        # Unexpected error during chat; print traceback for debugging and continue.
        print("An unexpected error occurred while running chat.")
        time.sleep(0.1)
        continue
    finally:
        try:
            sys.stdin.flush()
        except Exception:
            pass
        time.sleep(0.1)