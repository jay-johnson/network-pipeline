#!/usr/bin/env python

import os
import sys
import datetime
import time
import socket


def listen_on_tcp_port():
    """listen_on_tcp_port

    Run a simple server for processing messages over ``TCP``.

    ``LISTEN_ON_HOST`` - listen on this host ip address
    ``LISTEN_ON_PORT`` - listen on this ``TCP`` port
    ``LISTEN_SIZE`` - listen on to packets of this size
    ``LISTEN_SLEEP`` - sleep this number of seconds per loop
    ``LISTEN_SHUTDOWN_HOOK`` - shutdown if file is found on disk

    """

    host = os.getenv(
        "LISTEN_ON_HOST",
        "127.0.0.1").strip().lstrip()
    port = int(os.getenv(
        "LISTEN_ON_PORT",
        "80").strip().lstrip())
    backlog = int(os.getenv(
        "LISTEN_BACKLOG",
        "5").strip().lstrip())
    size = int(os.getenv(
        "LISTEN_SIZE",
        "1024").strip().lstrip())
    sleep_in_seconds = float(os.getenv(
        "LISTEN_SLEEP",
        "0.5").strip().lstrip())
    shutdown_hook = os.getenv(
        "LISTEN_SHUTDOWN_HOOK",
        "/tmp/shutdown-listen-server-{}-{}".format(
            host,
            port)).strip().lstrip()

    if os.path.exists(shutdown_hook):
        print(("Please remove the shutdown hook file: "
               "\nrm -f {}")
              .format(
                shutdown_hook))
        sys.exit(1)

    now = datetime.datetime.now().isoformat()
    print(("{} - Starting Server address={}:{} "
           "backlog={} size={} sleep={} shutdown={}")
          .format(
            now,
            host,
            port,
            backlog,
            size,
            sleep_in_seconds,
            shutdown_hook))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(backlog)

    msg = 0
    while 1:
        client, address = s.accept()
        send_data = False
        data = None
        while not data:
            data = client.recv(size)
            if data:
                now = datetime.datetime.now().isoformat()
                print(("{} received msg={} "
                       "data={} replying")
                      .format(
                        now,
                        msg,
                        data))
                msg += 1
                if msg > 1000000:
                    msg = 0

                send_data = True
            else:
                time.sleep(sleep_in_seconds)

        if send_data:
            client.send(data)
        if os.path.exists(shutdown_hook):
            now = datetime.datetime.now().isoformat()
            print(("{} detected shutdown "
                   "file={}")
                  .format(
                    now,
                    shutdown_hook))

        client.close()
    # end of loop
# end of listen_on_tcp_port


if __name__ == '__main__':
    listen_on_tcp_port()
