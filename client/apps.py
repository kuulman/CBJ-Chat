import customtkinter as tk
import components.chat as chat
from tkinter import messagebox
import asyncio
import websockets

async def connect():
    try:
        await websockets.connect("ws://localhost:8080")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

# Window setup
root = tk.CTk()
root.title("Chat Kernel 1.0")
root.geometry("200x300")
tk.set_appearance_mode('system')

# Logo
logo = tk.CTkLabel(root, text="Chat Kernel Beta", font=("Arial", 20, ))
logo.pack(pady=(8,0))
skmt_logo = tk.CTkLabel(root, text="Developed by SKMT", font=("Arial", 10, ))
skmt_logo.pack(pady=(0,10))

# Message
label = tk.CTkLabel(root, text="Message to:")
label.pack(anchor="w", pady=(1, 00), padx=(30, 0))
entry = tk.CTkEntry(root)
entry.pack(pady=1)

# Username
label2 = tk.CTkLabel(root, text="Username:")
label2.pack(anchor="w", pady=(1, 00), padx=(30, 0))
entry2 = tk.CTkEntry(root)
entry2.pack(pady=(1, 5))

# Tombol
button = tk.CTkButton(root, text="Chat", command=asyncio.create_task(connect))
button.pack(pady=10)

root.mainloop()
