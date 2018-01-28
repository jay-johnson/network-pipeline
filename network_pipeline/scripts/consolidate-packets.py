#!/usr/bin/env python

import os
import sys
import logging
import socket
import datetime
import time
import json
from network_pipeline.consts import INCLUDED_IGNORE_KEY
from network_pipeline.consts import VALID
from network_pipeline.consts import TCP
from network_pipeline.consts import UDP
from network_pipeline.consts import ICMP
from network_pipeline.consts import ARP
from network_pipeline.log.setup_logging import setup_logging
from network_pipeline.utils import ppj

# from celery_connectors.publisher import Publisher

setup_logging()

# consolidator - receives packets from network agents
name = "cdr"
log = logging.getLogger(name)

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
            "102400").strip().lstrip())
sleep_in_seconds = float(os.getenv(
            "LISTEN_SLEEP",
            "0.5").strip().lstrip())
needs_response = bool(os.getenv(
            "LISTEN_SEND_RESPONSE",
            "0").strip().lstrip() == "1")
shutdown_hook = os.getenv(
            "LISTEN_SHUTDOWN_HOOK",
            "/tmp/shutdown-listen-server-{}-{}".format(host,
                                                       port)).strip().lstrip()
filter_key = os.getenv(
                "IGNORE_KEY",
                INCLUDED_IGNORE_KEY).strip().lstrip()

if os.path.exists(shutdown_hook):
    log.info(("Please remove the shutdown hook file: "
              "\nrm -f {}")
             .format(shutdown_hook))
    sys.exit(1)

default_filter_key = filter_key
bytes_for_filter_key = len(default_filter_key)
offset_to_filter_key = (-1 * bytes_for_filter_key)
offset_to_msg = offset_to_filter_key - 1

now = datetime.datetime.now().isoformat()
log.info(("{} - Starting Server address={}:{} "
          "backlog={} size={} sleep={} shutdown={} "
          "filter_key={}")
         .format(now,
                 host,
                 port,
                 backlog,
                 size,
                 sleep_in_seconds,
                 shutdown_hook,
                 default_filter_key))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)
client, address = s.accept()

midx = 0
while 1:
    data = None
    address = None
    ignore_key = None

    try:
        if not client:
            client, address = s.accept()
    except Exception as e:
        log.error(("socket accept with ex={}")
                  .format(e))
    try:
        if client:
            data = client.recv(size)
    except Exception as e:
        log.error(("recv - disconnected with ex={}")
                  .format(e))
    if data:
        now = datetime.datetime.now().isoformat()
        packet_to_process = data[0:offset_to_msg]
        ignore_key = data[offset_to_filter_key:]
        log.info(("decoding data={} key={}")
                 .format(packet_to_process,
                         ignore_key))

        msg = None
        try:
            msg = json.loads(
                        packet_to_process.decode("utf-8"))
        except Exception as e:
            msg = None
            log.error(("Invalid data={} with ex={}")
                      .format(packet_to_process,
                              e))

        if msg:
            target_data = None
            hex_data = None

            log.info(("received msg={} "
                      "data={} replying - ignore='{}'")
                     .format(ppj(msg),
                             packet_to_process,
                             ignore_key))

            if msg["status"] == VALID:
                if msg["data_type"] == TCP:
                    log.info("TCP")
                elif msg["data_type"] == UDP:
                    log.info("TCP")
                elif msg["data_type"] == ARP:
                    log.info("TCP")
                elif msg["data_type"] == ICMP:
                    log.info("TCP")
                else:
                    log.error(("unsuppported type={}")
                              .format(msg["data_type"]))
                # end of supported eth protocol message types
            else:
                log.error(("unsuppported msg status={}")
                          .format(msg["status"]))
            # end if msg was VALID
        # end of if found msg

        midx += 1
        if midx > 1000000:
            midx = 0
    else:
        log.debug("ignoring invalid data")
    # end of if valid msg or not

    if needs_response:
        client.send(ignore_key)
    else:
        log.info("no response")
        time.sleep(sleep_in_seconds)

    if os.path.exists(shutdown_hook):
        now = datetime.datetime.now().isoformat()
        log.info(("{} detected shutdown "
                  "file={}")
                 .format(now,
                         shutdown_hook))
# end of loop

log.info("shutting down")
client.close()

log.info("done")
