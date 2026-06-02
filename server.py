import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind((SERVER_IP, SERVER_PORT))

print(f"Server port {SERVER_PORT}...")

clients = {}

while True:
    data, addr = server.recvfrom(1024)
    message = data.decode()

   
    if message.startswith("REGISTER:"):
        username = message.split(":")[1]

        clients[addr] = username

        print(f"{username} masuk ke room")

        # Broadcast join message
        for client_addr in clients:
            if client_addr != addr:
                notif = f"[SERVER] {username} telah bergabung ke room chat"
                server.sendto(notif.encode(), client_addr)

        continue

    
    if message == "LEAVE":
        username = clients.get(addr, "Unknown")

        print(f"{username} keluar dari room")

        if addr in clients:
            del clients[addr]

        for client_addr in clients:
            notif = f"[SERVER] {username} telah keluar dari room chat"
            server.sendto(notif.encode(), client_addr)

        continue

    username = clients.get(addr, "Unknown")

    print(f"{username}: {message}")

    for client_addr in clients:
        if client_addr != addr:
            send_message = f"{username}: {message}"
            server.sendto(send_message.encode(), client_addr)