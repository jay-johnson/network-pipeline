#!/usr/bin/env python

import logging
import scapy.all as scapy
from celery_connectors.utils import ev
from network_pipeline.log.setup_logging import setup_logging
from network_pipeline.handle_packets import handle_packets


setup_logging()
# scapy capture agent
name = "cap"
log = logging.getLogger(name)

dev = ev("CAP_DEVICE",
         "lo")

"""
Ignore ports for forwarding to consolidators:

Redis Internal VM: 6379, 16379
RabbitMQ Internal VM: 5672, 15672, 25672
"""

# http://biot.com/capstats/bpf.html
custom_filter = ("(udp and portrange 10000-17001) "
                 "or (tcp and portrange 80) "
                 "or arp "
                 "or icmp")

log.info(("starting device={} filter={}")
         .format(dev,
                 custom_filter))


scapy.sniff(
            filter=custom_filter,
            prn=handle_packets)

log.info("done")
