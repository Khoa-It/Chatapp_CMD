import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_server = int(input("Create Port:"))
server.bind(("0.0.0.0", port_server))
server.listen()

clients = {}

print("server running...")

def handle_clients(client):
    try:
       
        data = client.recv(1024).decode().strip()
        
        if data.startswith("GET") or data.startswith("POST") or len(data) > 20:
            print(f"[Warning] Block Bot.")
            client.close()
            return

        username, user_color = data.split("|", 1)
        clients[client] = {"name": username, "color": user_color}

        print(f"[System] {username} connected with color: {user_color}")
        broadcast(f'<b>{username} joined</b>'.encode(), client)

        while True:
            msg = client.recv(1024).decode()
            
            if not msg:
                break
            
            if msg == "p@i@n@g":
                continue

            color_msg = f'<style fg="{user_color}">[{username}]:</style> {msg}'
            broadcast(color_msg.encode(), client)
    except :
        pass

    finally:
        user_info = clients.get(client, {"name": "unknown"})
        username = user_info["name"]
        
        if client in clients:
            clients.pop(client)
            
        client.close()
        broadcast(f'<b>{username} leave</b>'.encode(), client)

   
def broadcast(message, sender):
    for c in list(clients.keys()):
        if c != sender:
            try:
                c.send(message)
            except:
                c.close()
                clients.pop(c, None)

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_clients, args=(client,), daemon=True).start() 
