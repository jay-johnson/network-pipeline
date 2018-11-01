#!/usr/bin/env python

import os
import netifaces
import kamene.all as kamene


def send_arp_msg():
    """send_arp_msg

    Send an ``ARP`` message to the network device (``enp0s3`` by default).

    """

    dev = os.getenv(
            "ARP_INTERFACE",
            "enp0s3").strip().lstrip()
    network_details = netifaces.ifaddresses(
            dev)
    dst_ip = os.getenv(
            "ARP_DST_IP",
            network_details[2][0]["addr"])
    dst_mac = os.getenv(
            "ARP_DST_MAC",
            network_details[17][0]["addr"])

    print(("Sending ARP to mac={} ip={}")
          .format(
            dst_mac,
            dst_ip))

    answered, unanswered = kamene.srp(
                            kamene.Ether(
                                dst=dst_mac
                            ) / kamene.ARP(
                                pdst=dst_ip
                            ),
                            timeout=2,
                            verbose=False)

    if len(answered) > 0:
        print(answered[0][0].getlayer(
            kamene.ARP
        ).pdst + " is up")
    elif len(unanswered) > 0:
        print(unanswered[0].getlayer(
            kamene.ARP
        ).pdst + " is down")

# end of send_arp_msg


if __name__ == "__main__":
    send_arp_msg()
