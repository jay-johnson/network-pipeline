#!/usr/bin/env python

import os
import socket
import uuid
import datetime


def send_udp_message():
    """send_udp_message

    Send a ``UDP`` message to port 80 by default.

    Environment variables:

    ``UDP_SEND_TO_HOST`` - host ip address
    ``UDP_SEND_TO_PORT`` - send to this UDP port

    """
    host = os.getenv(
        "UDP_SEND_TO_HOST",
        "0.0.0.0").strip().lstrip()
    port = int(os.getenv(
        "UDP_SEND_TO_PORT",
        "17000").strip().lstrip())

    need_response = os.getenv("NEED_RESPONSE", "0") == "1"

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
        print(data)
    client.close()
# end of send_udp_message


if __name__ == '__main__':
    send_udp_message()
