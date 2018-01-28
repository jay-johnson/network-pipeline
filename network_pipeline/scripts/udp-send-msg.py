#!/usr/bin/env python

import os
import socket
import uuid
import datetime

host = os.getenv(
            "UDP_SEND_TO_HOST",
            "0.0.0.0").strip().lstrip()
port = int(os.getenv(
            "UDP_SEND_TO_PORT",
            "17000").strip().lstrip())

need_response = os.getenv("NEED_RESPONSE", "0") == "1"

if __name__ == '__main__':
    msg = os.getenv(
            "MSG",
            "testing UDP msg time={} - {}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                uuid.uuid4()))

    server_address = (host, port)

    client = socket.socket(socket.AF_INET,
                           socket.SOCK_DGRAM)

    print(("sending UDP: "
           "address={} msg={}")
          .format(server_address,
                  msg))
    client.sendto(msg.encode(), server_address)
    if need_response:
        data = client.recv(1024).decode()
    client.close()
