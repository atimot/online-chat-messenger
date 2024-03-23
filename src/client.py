import socket
import sys
import os
import json
from pathlib import Path

class Client:
    SERVER_ADDRESS = '172.18.0.3'
    SERVER_PORT = 9001
    STREAM_RATE = 1400

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Connecting to {}'.format(self.SERVER_ADDRESS, self.SERVER_PORT))
    
    def start(self):
        try:
            self.sock.connect((self.SERVER_ADDRESS, self.SERVER_PORT))
        except socket.error as err:
            print(err)
            sys.exit(1)

        try:
            method_type = input("Type a conversion method: ")
            with open("ffmpeg_methods.json", "r") as f:
                methods = json.load(f)
            if not method_type in methods:
                print("Error {} is invalid method".format(method_type))
                sys.exit(1)
            method = methods[method_type]
            json_size = len(json.dumps(method).encode())

            file_path = input("Type in a file to upload: ")
            media_type = Path(file_path).suffix
            media_type_size = len(media_type.encode())

            with open(file_path, "rb") as f:
                f.seek(0, os.SEEK_END)
                file_size = f.tell()
                f.seek(0, 0)
                
                header = json_size.to_bytes(16, "big") + media_type_size.to_bytes(1, "big") + file_size.to_bytes(47, "big")
                body = json.dumps(method).encode() + media_type.encode() + f.read()

            self.sock.send(header)
            self.sock.send(body)

        finally:
            print("Closing socket")
            self.sock.close()

client = Client()
client.start()
