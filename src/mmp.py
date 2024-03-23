import json
import sys
import os

class MultipleMediaProtocol():
    HEADER_SIZE = 64

    def __init__(self) -> None:
        self.json_size = 0
        self.media_type_size = 0
        self.payload_size = 0
        self.media_type = ""
        self.payload = b""

    def set_body(self, json_data, media_type, file_data):
        self.json_size = int.from_bytes(json.dumps(json_data).encode())
        self.media_type_size = int.from_bytes(media_type.encode())
        self.payload_size = file_data.seek(0)
