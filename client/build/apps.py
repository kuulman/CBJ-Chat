import customtkinter as ctk
from tkinter import messagebox
import asyncio
import websockets

def checkCB():
    if user_entry.get().strip() == "":
        messagebox.showwarning("Error", "Username cannot be empty!")
        user_entry.focus()
        return
    else:
        messagebox.showinfo("Info", f"Connecting as {user_entry.get()}...")

# === Setup dasar ===
ctk.set_appearance_mode("system")  # "light", "dark", atau "system"
ctk.set_default_color_theme("blue")  # bisa juga "green", "dark-blue", dll.

# === Window ===
root = ctk.CTk()
root.title("Chat Kernel 1.0")
root.geometry("340x420")
root.resizable(False, False)

# === Frame utama (background) ===
main_frame = ctk.CTkFrame(root, corner_radius=20, fg_color=("#F5F6FA", "#2C2C2C"))
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# === Logo / Header ===
title_label = ctk.CTkLabel(
    main_frame,
    text="Welcome!",
    font=ctk.CTkFont("Inter", 30, "bold"),
)
title_label.pack(pady=(15, 5))

subtitle_label = ctk.CTkLabel(
    main_frame,
    text="Developed by SKMT",
    font=ctk.CTkFont("Inter", 12),
    text_color=("gray20", "gray80"),
)
subtitle_label.pack(pady=(0, 20))

# === Input: Username ===
user_label = ctk.CTkLabel(main_frame, text="Your Username:", anchor="w")
user_label.pack(fill="x", padx=25)
user_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Enter your username...",
    height=36,
    corner_radius=10,
)
user_entry.pack(padx=25, pady=(5, 25), fill="x")

# === Tombol ===
chat_button = ctk.CTkButton(
    main_frame,
    text="Start Chat",
    height=40,
    corner_radius=12,
    fg_color=("#0078FF", "#1F6AA5"),
    hover_color=("#0066DD", "#1A5A91"),
    command=lambda: messagebox.showinfo("Chat", f"Connecting as {user_entry.get()}...")
)
chat_button.pack(padx=25, pady=(0, 10), fill="x")

# === Footer ===
footer_label = ctk.CTkLabel(
    main_frame,
    text="© 2025 SKMT Labs",
    font=ctk.CTkFont(size=10),
    text_color=("gray40", "gray70"),
)
footer_label.pack(side="bottom", pady=(10, 5))

# === Jalankan UI ===
root.mainloop()
