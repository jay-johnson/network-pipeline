#!/usr/bin/env python

import logging
import scapy.all as scapy
from celery_connectors.utils import ev
from network_pipeline.log.setup_logging import setup_logging
from network_pipeline.handle_packets import handle_packets


setup_logging()
# scapy capture agent
name = "cap-udp"
log = logging.getLogger(name)

dev = ev("CAP_DEVICE",
         "lo")

"""
Ignore ports for forwarding to consolidators:

Redis VM: 6379, 16379
RabbitMQ VM: 5672, 15672, 25672

"""

# http://biot.com/capstats/bpf.html
default_filter = "udp"
custom_filter = ev("NETWORK_FILTER",
                   default_filter)

log.info(("starting device={} filter={}")
         .format(dev,
                 custom_filter))

scapy.sniff(
            filter=custom_filter,
            prn=handle_packets)

log.info("done")
