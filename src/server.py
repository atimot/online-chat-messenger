# サーバーを起動する時に自分のIPアドレスを出力する
# ポートは9001
import socket
import os
from pathlib import Path
import hashlib
import mimetypes

class Server:
    SERVER_ADDRESS = '0.0.0.0'
    SERVER_PORT = 9001
    STREAM_RATE = 1400

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.dpath = 'temp'
        if not os.path.exists(self.dpath):
            os.makedirs(self.dpath)

        ip = socket.gethostbyname(socket.gethostname())
        print('Starting up on {} port {}'.format(ip, self.SERVER_PORT))

        self.sock.bind((self.SERVER_ADDRESS, self.SERVER_PORT))
        self.sock.listen(1)

    def start(self):
        try:
            while True:
                connection, client = self.sock.accept()

                try:
                    header = connection.recv(64)
                    json_size = int.from_bytes(header[:16], "big")
                    media_type_size = int.from_bytes(header[16:17], "big")
                    payload_size = int.from_bytes(header[17:64], "big")

                    print(json_size)
                    print(media_type_size)
                    print(payload_size)

                    json_data = connection.recv(json_size)
                    media_type_data = connection.recv(media_type_size)
                    data_length = payload_size
                    with open(os.path.join(self.dpath, "hoge.mp4"), 'wb+') as f:
                        while data_length > 0:
                            data = connection.recv(data_length if data_length <= self.STREAM_RATE else self.STREAM_RATE)
                            
                            if not data:
                                break
                            
                            f.write(data)
                            data_length -= len(data)

                    print(json_data.decode())
                    print(media_type_data.decode())
                except Exception as e:
                    print(e)
                finally:
                    connection.close()
                    print("Closed connecton")

        finally:
            self.sock.close()
            print("Closed socket")


server = Server()
server.start()
