#!/usr/bin/env python

import os
import socket
import struct
import netifaces
from binascii import unhexlify

interface_name = os.getenv(
    "ARP_INTERFACE",
    "lo").strip().lstrip()
network_details = netifaces.ifaddresses(
    interface_name)
ipaddress = network_details[2][0]['addr']
macaddress = network_details[17][0]['addr']


class Ethernet(object):

    def __init__(self):
        self.dst = None
        self.src = None
        self.etype = None


class Arp(object):

    def __init__(self):
        self.htype = None
        self.ptype = None
        self.hsize = None
        self.psize = None
        self.op = None
        self.shwa = None
        self.spa = None
        self.thwa = None
        self.tpa = None
        self.padd = None


host = os.getenv(
            "UDP_LISTEN_ON_HOST",
            "127.0.0.1").strip().lstrip()
port = int(os.getenv(
            "UDP_LISTEN_ON_PORT",
            "17000").strip().lstrip())

need_response = os.getenv("NEED_RESPONSE", "0") == "1"

if __name__ == "__main__":
    server_address = (host, port)

    eth = Ethernet()
    eth.dst = unhexlify("ffffffffffff")
    eth.src = unhexlify("e09d312efe3c")  # your NIC MAC
    eth.etype = 806

    arp = Arp()
    arp.htype = 0x01  # 2 bytes
    arp.ptype = 0x0800  # 2 bytes
    arp.hsize = 0x06  # 1 byte
    arp.psize = 0x04  # 1 byte
    arp.op = 0x01  # 2 bytes
    arp.shwa = unhexlify("e09d312efe3c")   # your NIC MAC
    arp.spa = socket.inet_aton("192.168.0.56")   # your host IP
    arp.thwa = unhexlify("000000000000")
    arp.padd = unhexlify("49206c6f7665206e6574776f726b696e6721")

    # should be any IP from your network if
    # hen using the same IP as you host you will send GARP
    arp.tpa = socket.inet_aton("192.168.0.38")

    eth_frame = struct.pack(
                        "!6s6sH",
                        eth.dst,
                        eth.src,
                        eth.etype)

    arp_frame = struct.pack(
                        "!HHBBH6s4s6s4s18s",
                        arp.htype,
                        arp.ptype,
                        arp.hsize,
                        arp.psize,
                        arp.op,
                        arp.shwa,
                        arp.spa,
                        arp.thwa,
                        arp.tpa,
                        arp.padd)

    print("creating ARP packet")
    arp_packet = eth_frame + arp_frame

    print("creating socket")
    s = socket.socket(socket.PF_PACKET,
                      socket.SOCK_RAW,
                      socket.htons(0x800))

    print("binding socket")
    s.bind((interface_name, 0))

    s.send(arp_packet)
