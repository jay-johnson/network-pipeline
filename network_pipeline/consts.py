import os
import struct
import json


SOURCE = os.getenv(
    "SOURCE_HOST",
    "localdev").strip().lstrip()
FORWARD_BROKER_URL = os.getenv(
    "FORWARD_BROKER_URL",
    "redis://localhost:6379/15").strip().lstrip()
FORWARD_SSL_OPTIONS = json.loads(os.getenv(
    "FORWARD_SSL_OPTIONS",
    "{}").strip().lstrip())
FORWARD_ENDPOINT_TYPE = os.getenv(
    "FORMAT_ET",
    "redis").strip().strip()
FORWARD_EXCHANGE = os.getenv(
    "FORWARD_EXCHANGE",
    "NEW_PACKETS").strip().lstrip()
FORWARD_ROUTING_KEY = os.getenv(
    "FORWARD_ROUTING_KEY",
    "NEW_PACKETS").strip().lstrip()
FORWARD_QUEUE = os.getenv(
    "FORWARD_QUEUE",
    "NEW_PACKETS").strip().lstrip()
DEBUG_PACKETS = bool(os.getenv(
    "DEBUG_PACKETS",
    "0").strip().lstrip() == "1")

# Prototype engine - for filtering off message contents
# not just src/dst ip and protocols
# not functional for all cases yet

INCLUDED_IGNORE_KEY = "CHANGE_TO_YOUR_OWN_KEY"

ETH_HEADER_FORMAT = "!6s6sH"
IP_HEADER_FORMAT = "!BBHHHBBH4s4s"
TCP_HEADER_FORMAT = "!HHLLBBHHH"
TCP_PSH_FORMAT = "!4s4sBBH"
UDP_HEADER_FORMAT = "!HHHH"
ICMP_HEADER_FORMAT = "!BBH"
ARP_HEADER_FORMAT = "2s2s1s1s2s6s4s6s4s"

SIZE_ETH_HEADER = struct.calcsize(ETH_HEADER_FORMAT)
SIZE_IP_HEADER = struct.calcsize(IP_HEADER_FORMAT)
SIZE_TCP_HEADER = struct.calcsize(TCP_HEADER_FORMAT)
SIZE_UDP_HEADER = struct.calcsize(UDP_HEADER_FORMAT)
SIZE_ICMP_HEADER = struct.calcsize(ICMP_HEADER_FORMAT)
SIZE_ARP_HEADER = struct.calcsize(ARP_HEADER_FORMAT)

VALID = 0
FILTERED = 1
INVALID = 2
ERROR = 3
UNSUPPORTED = 4
ETH_UNSUPPORTED = 5
IP_UNSUPPORTED = 6

UNKNOWN = 0
TCP = 1
UDP = 2
ICMP = 3
ARP = 4

ARP_PROTO_ETH = 9731
ICMP_PROTO_IP = 1
IP_PROTO_ETH = 8
TCP_PROTO_IP = 6
UDP_PROTO_IP = 17

IGNORED_REDIS_PORTS = [6379, 16379]
IGNORED_RABBITMQ_PORTS = [5672, 15672, 25672]
