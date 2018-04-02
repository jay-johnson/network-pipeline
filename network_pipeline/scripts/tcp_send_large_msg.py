#!/usr/bin/env python

import os
import socket
import uuid
import datetime


def send_tcp_large_message():
    """send_tcp_large_message

    Send a large ``TCP`` message to port 80 by default.

    """

    need_response = os.getenv("NEED_RESPONSE", "0") == "1"

    msg = os.getenv(
            "MSG",
            "testing msg time={} - {}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                uuid.uuid4()))
    host = "127.0.0.1"
    port = 80

    client = socket.socket()
    client.connect((host, port))

    msg += " large_random_data="
    for i in range(0, 100):
        for j in range(0, 100):
            msg += str(uuid.uuid4())

    print(("sending LARGE msg: {}")
          .format(len(msg)))
    client.sendall(msg.encode())
    if need_response:
        data = client.recv(1024).decode()
        print(data)
    client.close()
# end of send_tcp_large_message


if __name__ == '__main__':
    send_tcp_large_message()
