#!/usr/bin/env python3
"""Test client B — connects, waits a short moment, sends a reply, then listens and exits."""
import asyncio
import os
import json
import base64
from datetime import datetime, timezone

try:
    from Crypto.Cipher import AES
except Exception:
    AES = None

import websockets


async def run():
    uri = "ws://localhost:8080"
    userId = "B"
    print(f"[{userId}] Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print(f"[{userId}] Connected")

            async def receiver():
                try:
                    async for message in websocket:
                        print(f"[{userId}] Received raw: {message}")
                except websockets.ConnectionClosed:
                    print(f"[{userId}] Connection closed")

            recv_task = asyncio.create_task(receiver())

            # wait for partner to send first
            await asyncio.sleep(0.5)

            msg = {
                "userId": userId,
                "message": "Reply from client B",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

            AES_KEY = os.getenv("AES_KEY")
            iv = os.getenv("iv")
            if AES and AES_KEY and iv:
                key = AES_KEY.encode("utf-8")
                ivb = iv.encode("utf-8")
                raw = json.dumps(msg).encode("utf-8")
                block_size = 16
                padding_length = block_size - (len(raw) % block_size)
                raw += bytes([padding_length]) * padding_length
                cipher = AES.new(key, AES.MODE_CBC, ivb)
                encrypted = cipher.encrypt(raw)
                payload = base64.b64encode(encrypted)
                await websocket.send(payload)
                print(f"[{userId}] Sent encrypted message (base64)")
            else:
                await websocket.send(json.dumps(msg))
                print(f"[{userId}] Sent plaintext JSON message")

            await asyncio.sleep(2)
            recv_task.cancel()
    except ConnectionRefusedError:
        print(f"[{userId}] Connection refused — server may be offline")


if __name__ == '__main__':
    asyncio.run(run())
