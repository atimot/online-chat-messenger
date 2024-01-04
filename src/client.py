import socket
import threading

class Client:
    SERVER_ADDRESS = '172.18.0.4'
    SERVER_PORT = 9001
    SERVER = (SERVER_ADDRESS, SERVER_PORT)

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.username = ""
        self.usernamelen = 0

    def create_message(self, message=""):
        return self.usernamelen.to_bytes(1, "big") + self.username.encode("utf-8") + message.encode("utf-8")

    def login(self):
        self.username = input("Type username\n")
        self.usernamelen = len(self.username.encode("utf-8"))
        message = self.create_message()
        self.sock.sendto(message, self.SERVER)
    
    def start(self):
        threading.Thread(target=self.recv_data).start()

        while True:
            message = self.create_message(input())
            self.sock.sendto(message, self.SERVER)

    def close(self):
        print("Close client connection")
        self.sock.close()

    def recv_data(self):
        while True:
            try:
                data, _ = self.sock.recvfrom(4096)

                if data:
                    data = data.decode("utf-8")
                    print(data)
            except Exception:
                break

client = Client()
try:
    client.login()
    client.start()
finally:
    client.close()
