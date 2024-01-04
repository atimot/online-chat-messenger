import socket
from datetime import datetime, timedelta
import threading

class Server:
    SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
    SERVER_PORT = 9001

    def __init__(self):
        self.clients = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.SERVER_ADDRESS, self.SERVER_PORT))

    def start(self):
        print("Starting server {}".format(self.SERVER_ADDRESS))
        while True:
            data, client_address = self.sock.recvfrom(4096)

            usernamelen = int.from_bytes(data[:1], "big")
            username = data[1:1 + usernamelen].decode("utf-8")
            message = data[1 + usernamelen:].decode("utf-8")

            # 初回メッセージのみここを通る想定
            if username not in self.clients:
                self.clients[username] = {
                    "name": username,
                    "address": client_address,
                    "last_recived_at": datetime.now()
                }
                print("New user connected: {}".format(username))
                continue
            
            self.clients[username]["last_recived_at"] = datetime.now()
            for _, client in self.clients.items():
                if not client["name"] == username:
                    send_message = '{}:{}'.format(username, message)
                    self.sock.sendto(send_message.encode(), client["address"])

    def clean_up(self):
        while True:
            over_time = datetime.now() - timedelta(seconds=60)

            clients = self.clients
            for key, client in list(clients.items()):
                if client["last_recived_at"] < over_time:
                    print("Client {} is over".format(client["name"]))
                    clients.pop(key)

server = Server()
threading.Thread(target=server.clean_up).start()
server.start()
