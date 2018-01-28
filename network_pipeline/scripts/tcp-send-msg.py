#!/usr/bin/env python

import os
import socket
import uuid
import datetime

need_response = os.getenv("NEED_RESPONSE", "0") == "1"

if __name__ == '__main__':
    msg = os.getenv(
            "MSG",
            "testing msg time={} - {}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                uuid.uuid4()))
    host = "127.0.0.1"
    port = 80

    client = socket.socket()
    client.connect((host, port))

    print(("sending: {}")
          .format(msg))
    client.send(msg.encode())
    if need_response:
        data = client.recv(1024).decode()
    client.close()
