#!/usr/bin/env python

import os
import netifaces
import scapy.all as scapy


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
      .format(dst_mac,
              dst_ip))

answered, unanswered = scapy.srp(
                        scapy.Ether(
                            dst=dst_mac
                        ) / scapy.ARP(
                            pdst=dst_ip
                        ),
                        timeout=2,
                        verbose=False)

if len(answered) > 0:
    print(answered[0][0].getlayer(
        scapy.ARP
    ).pdst + " is up")
elif len(unanswered) > 0:
    print(unanswered[0].getlayer(
        scapy.ARP
    ).pdst + " is down")
