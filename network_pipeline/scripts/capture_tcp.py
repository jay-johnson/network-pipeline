#!/usr/bin/env python

import scapy.all as scapy
from spylunking.log.setup_logging import console_logger
from celery_connectors.utils import ev
from network_pipeline.handle_packets import handle_packets


log = console_logger(
    name='cap_tcp')


def capture_tcp_packets():
    """capture_tcp_packets

    Capture ``TCP`` packets and call the ``handle_packets`` method

    Change the network interface by ``export CAP_DEVICE=eth0``

    """
    dev = ev(
        "CAP_DEVICE",
        "lo")

    """
    Ignore ports for forwarding to consolidators:

    Redis VM: 6379, 16379
    RabbitMQ VM: 5672, 15672, 25672

    """

    # http://biot.com/capstats/bpf.html
    default_filter = ("tcp and ( port 80 or port 443 "
                      "or port 8010 or port 8443 )")
    custom_filter = ev(
        "NETWORK_FILTER",
        default_filter)

    log.info(("starting device={} filter={}")
             .format(
                dev,
                custom_filter))

    scapy.sniff(
        filter=custom_filter,
        prn=handle_packets)

    log.info("done")

# end of capture_tcp_packets


if __name__ == "__main__":
    capture_tcp_packets()
