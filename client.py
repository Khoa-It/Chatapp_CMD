import socket
import threading
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
import asyncio
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_server = input("IP Server: ")
port_server = int(input("Port: "))
client.connect((ip_server, port_server))


username = input("Enter your name: ")
client.send(username.encode())

# def notify_windows(msg):
#     code = f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('{msg}')"
#     # Hoặc dùng Toast Notification của Win10
#     ps_script = f'$notif = New-Object -ComObject WScript.Shell; $notif.Popup("{msg}", 3, "Chat App", 64)'
#     subprocess.Popen(["powershell", "-Command", ps_script], creationflags=subprocess.CREATE_NO_WINDOW)

def trigger_notification(message):
    # Gọi file exe chạy ngầm hoàn toàn
    try:
        subprocess.Popen(
            ["notif.exe", message],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        print(f"Không tìm thấy file notif.exe: {e}")

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:
                with patch_stdout():
                    print(msg)

                # notify_windows(msg)
                trigger_notification(msg)
        except:
            break

session = PromptSession()

def send_message():
    msg = session.prompt("You: ")
    client.send(msg.encode())

threading.Thread(target=receive, daemon= True).start()

while True:
   send_message() 
    
