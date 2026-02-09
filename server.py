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
        username = client.recv(1024).decode()
        clients[client] = username
        broadcast(f'{username} joined'.encode(),client)
        while True:
            msg = client.recv(1024).decode()
            if not msg:
                break
            broadcast(f"[{username}]: {msg}".encode(), client)

    except :
        pass

    finally:
        username = clients.get(client, "unknown")
        clients.pop(client, None)
        client.close()
        broadcast(f"{username} leave".encode(), client)

   
def broadcast(message, sender):
    for c in clients:
        if c!= sender:
            c.send(message)


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_clients, args=(client,), daemon=True).start() 
