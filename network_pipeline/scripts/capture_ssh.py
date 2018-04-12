#!/usr/bin/env python

import scapy.all as scapy
from celery_connectors.utils import ev
from network_pipeline.log.setup_logging import build_colorized_logger
from network_pipeline.handle_packets import handle_packets


name = "cap-ssh"
log = build_colorized_logger(
    name=name,
    config="capture-ssh-logging.json")


def capture_tcp_packets_over_ssh():
    """capture_tcp_packets_over_ssh

    Capture ``TCP`` packets over ssh
    and call the ``handle_packets`` method

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
    default_filter = ("tcp and ( port 22 )")
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

# end of capture_tcp_packets_over_ssh


if __name__ == "__main__":
    capture_tcp_packets_over_ssh()
