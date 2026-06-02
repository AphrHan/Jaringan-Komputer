import socket
import threading
import sys

USERNAME = input("Nama Kamu Siapa?: ")

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

register_message = f"REGISTER:{USERNAME}"
client.sendto(register_message.encode(), (SERVER_IP, SERVER_PORT))


def receive_messages():
    while True:
        try:
            data, _ = client.recvfrom(1024)
            print("\n" + data.decode())
        except:
            break


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

print(f"{USERNAME} Terhubung ke chatroom uhuy UDP!")
print("Ketik pesan untuk chat")
print("Ketik /leave untuk keluar\n")


while True:
    message = input()

    if message == "/leave":
        client.sendto("LEAVE".encode(), (SERVER_IP, SERVER_PORT))

        print("Anda keluar dari room chat.")

        client.close()
        sys.exit()

    client.sendto(
        message.encode(),
        (SERVER_IP, SERVER_PORT)
    )