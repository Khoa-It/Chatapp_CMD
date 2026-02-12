import warnings
# Tắt tất cả các cảnh báo từ thư viện requests/urllib3
warnings.filterwarnings("ignore", category=UserWarning, module='requests')
warnings.filterwarnings("ignore", message=".*urllib3.*")

import os
import requests
import sys
import socket
import threading
import subprocess
import time
import re
from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.patch_stdout import patch_stdout

GITHUB_RELEASE_URL = "https://github.com/Khoa-It/Chatapp_CMD/releases/latest/download/Chat_CMD.zip"

ip_server = input("IP Server: ")
port_server = int(input("Port: "))

# def notify_windows(msg):
#     code = f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('{msg}')"
#     # Hoặc dùng Toast Notification của Win10
#     ps_script = f'$notif = New-Object -ComObject WScript.Shell; $notif.Popup("{msg}", 3, "Chat App", 64)'
#     subprocess.Popen(["powershell", "-Command", ps_script], creationflags=subprocess.CREATE_NO_WINDOW)

def maintain_connection():
    global client
    while True:
        if client is None:
            client = connect_to_server(ip_server, port_server)
        else:
            try:
                # Gửi một tin nhắn "ping" nhỏ để check
                client.sendall(b'p@i@n@g')
            except:
                print("Kết nối bị ngắt, đang thử lại...")
                client = connect_to_server(ip_server, port_server)
        
        time.sleep(5) # Đợi 5 giây rồi check tiếp


def connect_to_server(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip, port))
        print("Connect successfull!")
        return client
    except Exception as e:
        print(f"Connect failed: {e}")
        return None

def update_from_github():
    try:
        print("Checking for updates...")
        app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        zip_path = os.path.join(app_dir, "update.zip")
        
        response = requests.get(GITHUB_RELEASE_URL, stream=True)
        response.raise_for_status()
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        current_file = sys.argv[0]
        updater_script = os.path.join(app_dir, "finish_update.bat")
        
        with open(updater_script, "w") as f:
            f.write(f"""
            @echo off
            timeout /t 2 /nobreak > nul
            powershell Expand-Archive -Path "{zip_path}" -DestinationPath "{app_dir}" -Force
            del "{zip_path}"
            start "" "{current_file}"
            del "%~f0"
            """)

        subprocess.Popen([updater_script], shell=True)
        print("Update downloaded. Restarting...")
        os._exit(0) 

    except Exception as e:
        print(f"Update failed: {e}")

def trigger_notification(message):
    # Gọi file exe chạy ngầm hoàn toàn
    clean_msg = re.sub(r'<[^>]+>', '', message)
    try:
        subprocess.Popen(
            ["notif.exe", clean_msg],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception:
        pass

def is_valid_hex_color(color_code):
    # Regex kiểm tra định dạng #RRGGBB (ví dụ: #FF5733)
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color_code)
    return match is not None

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:
                with patch_stdout():
                    print_formatted_text(HTML(msg))

                # notify_windows(msg)
                trigger_notification(msg)
        except:
            break



username = input("Enter your name: ")
while True:
    user_color = input("Enter your color (ví dụ #FF5733): ").strip()
    
    if is_valid_hex_color(user_color):
        print(f"Choose color successfull: {user_color}")
        break # Thoát vòng lặp nếu màu hợp lệ
    else:
        print("Enter valid color!")


client = connect_to_server(ip_server, port_server)

client.send(f"{username}|{user_color}".encode())
session = PromptSession()

def send_message():
    # Sử dụng session.prompt để lấy tin nhắn từ người dùng
    prompt_label = HTML(f'<style fg="{user_color}">[{username}]: </style>')
    msg = session.prompt(prompt_label)

    # Kiểm tra nếu người dùng gõ lệnh /update
    if msg.strip().lower() == "/update":
        with patch_stdout():
            print("\n[System] Checking latest version...")
        update_from_github() # Gọi hàm cập nhật của bạn
        return # Sau khi gọi update, hàm này sẽ thoát (hoặc app sẽ đóng để cập nhật)

    # Nếu không phải lệnh, gửi tin nhắn đi như bình thường
    client.send(msg.encode())

threading.Thread(target=receive, daemon= True).start()
threading.Thread(target=maintain_connection, daemon=True).start()

while True:
   send_message() 
    
