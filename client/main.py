from components.chat import chat
import asyncio
import sys
import time
import traceback


def prompt_session():
    try:
        return input("Enter session ID to join (e.g., 8080): ").strip()
    except EOFError:
        # EOF means no more input (e.g., user pressed Ctrl-D). Exit the loop.
        print("\nExiting.")
        return None


while True:
    try:
        input_session = prompt_session()
    except KeyboardInterrupt:
        print("\nExiting.")
        break

    if input_session is None:
        break

    if not input_session.isdigit():
        print("Invalid session ID. Please enter a numeric value.")
        continue

    try:
        asyncio.run(chat(input_session))
    except ConnectionRefusedError:
        # chat() already prints a friendly message when server is offline,
        # but handle residual ConnectionRefusedError here as well.
        time.sleep(0.1)
        continue
    except Exception:
        # Unexpected error during chat; print traceback for debugging and continue.
        print("An unexpected error occurred while running chat:")
        traceback.print_exc()
        time.sleep(0.1)
        continue
    finally:
        try:
            sys.stdin.flush()
        except Exception:
            pass
        time.sleep(0.1)