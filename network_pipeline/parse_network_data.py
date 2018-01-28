import logging
import uuid
import socket
import json
from struct import unpack
from network_pipeline.consts import ETH_HEADER_FORMAT
from network_pipeline.consts import IP_HEADER_FORMAT
from network_pipeline.consts import TCP_HEADER_FORMAT
from network_pipeline.consts import UDP_HEADER_FORMAT
from network_pipeline.consts import ICMP_HEADER_FORMAT
from network_pipeline.consts import ARP_HEADER_FORMAT
from network_pipeline.consts import SIZE_ETH_HEADER
from network_pipeline.consts import SIZE_IP_HEADER
from network_pipeline.consts import SIZE_TCP_HEADER
from network_pipeline.consts import SIZE_UDP_HEADER
from network_pipeline.consts import SIZE_ICMP_HEADER
from network_pipeline.consts import SIZE_ARP_HEADER
from network_pipeline.consts import VALID
from network_pipeline.consts import INVALID
from network_pipeline.consts import ERROR
from network_pipeline.consts import FILTERED
from network_pipeline.consts import UNKNOWN
from network_pipeline.consts import ETH_UNSUPPORTED
from network_pipeline.consts import IP_UNSUPPORTED
from network_pipeline.consts import TCP
from network_pipeline.consts import UDP
from network_pipeline.consts import ICMP
from network_pipeline.consts import ARP
from network_pipeline.consts import IP_PROTO_ETH
from network_pipeline.consts import ARP_PROTO_ETH
from network_pipeline.consts import TCP_PROTO_IP
from network_pipeline.consts import UDP_PROTO_IP
from network_pipeline.consts import ICMP_PROTO_IP
from network_pipeline.log.setup_logging import setup_logging

setup_logging()
name = "parser"
log = logging.getLogger(name)


# Get string of 6 characters as ethernet address into dash seperated hex string
def eth_addr(f):
    """eth_addr

    :param f: eth frame
    """
    data = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (f[0],
                                              f[1],
                                              f[2],
                                              f[3],
                                              f[4],
                                              f[5])
    return data
# end of eth_addr


def unshift_flags(tcp_flags):
    '''
    De-shift the TCP flags to a string repr
    '''
    return (tcp_flags & 0x01,
            (tcp_flags >> 1) & 0x01,
            (tcp_flags >> 2) & 0x01,
            (tcp_flags >> 3) & 0x01,
            (tcp_flags >> 4) & 0x01,
            (tcp_flags >> 5) & 0x01,)
# end of unshift_flags


def build_key():
    """build_key"""
    return str(uuid.uuid4())
# end of build_key


def parse_network_data(data_packet=None,
                       include_filter_key=None,
                       filter_keys=[],
                       record_tcp=True,
                       record_udp=True,
                       record_arp=True,
                       record_icmp=True):
    """build_node

    :param data_packet: raw recvfrom data
    :param filter_keys: list of strings to filter
                        and remove baby-birding
                        packets to yourself
    :param record_tcp: want to record TCP frames?
    :param record_udp: want to record UDP frames?
    :param record_arp: want to record ARP frames?
    :param record_icmp: want to record ICMP frames?
    """

    node = {"id": build_key(),
            "data_type": UNKNOWN,
            "eth_protocol": None,
            "eth_src_mac": None,
            "eth_dst_mac": None,
            "eth_length": SIZE_ETH_HEADER,
            "ip_version_ih1": None,
            "ip_version": None,
            "ip_ih1": None,
            "ip_hdr_len": None,
            "ip_tos": None,
            "ip_tlen": None,
            "ip_id": None,
            "ip_frag_off": None,
            "ip_ttl": None,
            "ip_protocol": None,
            "ip_src_addr": None,
            "ip_dst_addr": None,
            "tcp_src_port": None,
            "tcp_dst_port": None,
            "tcp_sequence": None,
            "tcp_ack": None,
            "tcp_resrve": None,
            "tcp_data_offset": None,
            "tcp_flags": None,
            "tcp_adwind": None,
            "tcp_urg_ptr": None,
            "tcp_ffin": None,
            "tcp_fsyn": None,
            "tcp_frst": None,
            "tcp_fpsh": None,
            "tcp_fack": None,
            "tcp_furg": None,
            "tcp_header_size": None,
            "tcp_data_size": None,
            "tcp_data": None,
            "udp_header_size": None,
            "udp_data_size": None,
            "udp_src_port": None,
            "udp_dst_port": None,
            "udp_data_len": None,
            "udp_csum": None,
            "udp_data": None,
            "icmp_header_size": None,
            "icmp_data": None,
            "icmp_type": None,
            "icmp_code": None,
            "icmp_csum": None,
            "icmp_data_size": None,
            "arp_header_size": None,
            "arp_data": None,
            "arp_hw_type": None,
            "arp_proto_type": None,
            "arp_hw_size": None,
            "arp_proto_size": None,
            "arp_opcode": None,
            "arp_src_mac": None,
            "arp_src_ip": None,
            "arp_dst_mac": None,
            "arp_dst_ip": None,
            "arp_data_size": None,
            "target_data": None,
            "full_offset": None,
            "eth_header_size": None,
            "ip_header_size": None,
            "err": "",
            "stream": None,
            "filtered": None,
            "status": INVALID}

    err = "no_data"
    if not data_packet:
        node["error"] = err
        return node

    try:

        err = "missing_packet"
        packet = data_packet[0]

        if len(packet) < 21:
            node["status"] = INVALID
            node["error"] = "invalid packet={}".format(packet)
            return node

        err = "failed_parsing_ethernet"
        eth_packet_min = 0
        eth_packet_max = eth_packet_min + node["eth_length"]

        log.info(("unpacking ETH[{}:{}]")
                 .format(eth_packet_min,
                         eth_packet_max))

        eth_datagram = packet[eth_packet_min:eth_packet_max]
        eth_header = unpack(ETH_HEADER_FORMAT, eth_datagram)
        node["eth_protocol"] = socket.ntohs(eth_header[2])
        node["eth_src_mac"] = eth_addr(packet[0:6])
        node["eth_dst_mac"] = eth_addr(packet[6:12])
        log.debug(("eth src={} dst={} proto={}")
                  .format(node["eth_src_mac"],
                          node["eth_dst_mac"],
                          node["eth_protocol"]))

        node["eth_header_size"] = SIZE_ETH_HEADER

        # Is this an IP packet:
        if node["eth_protocol"] == IP_PROTO_ETH:

            ip_packet_min = SIZE_ETH_HEADER
            ip_packet_max = SIZE_ETH_HEADER + 20

            log.info(("unpacking IP[{}:{}]")
                     .format(ip_packet_min,
                             ip_packet_max))

            err = ("failed_parsing_IP[{}:{}]").format(
                    ip_packet_min,
                    ip_packet_max)

            # take the first 20 characters for the IP header
            ip_datagram = packet[ip_packet_min:ip_packet_max]

            ip_header = unpack(IP_HEADER_FORMAT, ip_datagram)
            # https://docs.python.org/2/library/struct.html#format-characters

            node["ip_header_size"] = SIZE_IP_HEADER

            node["ip_version_ih1"] = ip_header[0]
            node["ip_version"] = node["ip_version_ih1"] >> 4
            node["ip_ih1"] = node["ip_version_ih1"] & 0xF
            node["ip_hdr_len"] = node["ip_ih1"] * 4
            node["ip_tos"] = ip_header[1]
            node["ip_tlen"] = ip_header[2]
            node["ip_id"] = ip_header[3]
            node["ip_frag_off"] = ip_header[4]
            node["ip_ttl"] = ip_header[5]
            node["ip_protocol"] = ip_header[6]
            node["ip_src_addr"] = socket.inet_ntoa(ip_header[8])
            node["ip_dst_addr"] = socket.inet_ntoa(ip_header[9])

            log.debug("-------------------------------------------")
            log.debug("IP Header - Layer 3")
            log.debug("")
            log.debug(" - Version: {}".format(node["ip_version"]))
            log.debug(" - HDR Len: {}".format(node["ip_ih1"]))
            log.debug(" - TOS: {}".format(node["ip_tos"]))
            log.debug(" - ID: {}".format(node["ip_id"]))
            log.debug(" - Frag: {}".format(node["ip_frag_off"]))
            log.debug(" - TTL: {}".format(node["ip_ttl"]))
            log.debug(" - Proto: {}".format(node["ip_protocol"]))
            log.debug(" - Src IP: {}".format(node["ip_src_addr"]))
            log.debug(" - Dst IP: {}".format(node["ip_dst_addr"]))
            log.debug("-------------------------------------------")
            log.debug("")

            tcp_data = None
            udp_data = None
            arp_data = None
            icmp_data = None
            target_data = None

            eh = node["eth_header_size"]
            ih = node["ip_header_size"]

            log.debug(("parsing ip_protocol={} data")
                      .format(node["ip_protocol"]))

            if node["ip_protocol"] == TCP_PROTO_IP:

                packet_min = node["eth_length"] + node["ip_hdr_len"]
                packet_max = packet_min + 20

                # unpack the TCP packet
                log.info(("unpacking TCP[{}:{}]")
                         .format(packet_min,
                                 packet_max))

                err = ("failed_parsing_TCP[{}:{}]").format(
                        packet_min,
                        packet_max)

                tcp_datagram = packet[packet_min:packet_max]

                log.debug(("unpacking TCP Header={}")
                          .format(tcp_datagram))

                # unpack the TCP packet
                tcp_header = unpack(TCP_HEADER_FORMAT, tcp_datagram)

                node["tcp_src_port"] = tcp_header[0]
                node["tcp_dst_port"] = tcp_header[1]
                node["tcp_sequence"] = tcp_header[2]
                node["tcp_ack"] = tcp_header[3]
                node["tcp_resrve"] = tcp_header[4]
                node["tcp_data_offset"] = node["tcp_resrve"] >> 4

                node["tcp_flags"] = tcp_header[5]
                node["tcp_adwind"] = tcp_header[6]
                node["tcp_urg_ptr"] = tcp_header[7]

                # parse TCP flags
                flag_data = unshift_flags(node["tcp_flags"])
                node["tcp_ffin"] = flag_data[0]
                node["tcp_fsyn"] = flag_data[1]
                node["tcp_frst"] = flag_data[2]
                node["tcp_fpsh"] = flag_data[3]
                node["tcp_fack"] = flag_data[4]
                node["tcp_furg"] = flag_data[5]

                # process the TCP options if there are
                # currently just skip it
                node["tcp_header_size"] = SIZE_TCP_HEADER

                log.debug(("src={} dst={} seq={} ack={} doff={} flags={} "
                           "f urg={} fin={} syn={} rst={} "
                           "psh={} fack={} urg={}")
                          .format(node["tcp_src_port"],
                                  node["tcp_dst_port"],
                                  node["tcp_sequence"],
                                  node["tcp_ack"],
                                  node["tcp_data_offset"],
                                  node["tcp_flags"],
                                  node["tcp_urg_ptr"],
                                  node["tcp_ffin"],
                                  node["tcp_fsyn"],
                                  node["tcp_frst"],
                                  node["tcp_fpsh"],
                                  node["tcp_fack"],
                                  node["tcp_furg"]))
                # --------------------------------------------------------
                err = "failed_tcp_data"

                node["data_type"] = TCP
                node["tcp_header_size"] = (
                        node["ip_hdr_len"] + (node["tcp_data_offset"] * 4))
                node["tcp_data_size"] = len(packet) - node["tcp_header_size"]
                th = node["tcp_header_size"]
                node["full_offset"] = eh + ih + th
                log.info(("TCP Data size={} th1={} th2={} "
                          "offset={} value={}")
                         .format(node["tcp_data_size"],
                                 node["ip_hdr_len"],
                                 node["tcp_header_size"],
                                 node["full_offset"],
                                 tcp_data))
                err = "failed_tcp_data_offset"
                tcp_data = packet[node["full_offset"]:]
                target_data = tcp_data
                node["error"] = ""
                node["status"] = VALID
            elif node["ip_protocol"] == UDP_PROTO_IP:

                packet_min = node["eth_length"] + node["ip_hdr_len"]
                packet_max = packet_min + 8

                # unpack the UDP packet
                log.info(("unpacking UDP[{}:{}]")
                         .format(packet_min,
                                 packet_max))

                err = ("failed_parsing_UDP[{}:{}]").format(
                        packet_min,
                        packet_max)

                udp_datagram = packet[packet_min:packet_max]

                log.info(("unpacking UDP Header={}")
                         .format(udp_datagram))

                udp_header = unpack(UDP_HEADER_FORMAT, udp_datagram)
                node["udp_header_size"] = SIZE_UDP_HEADER

                node["udp_src_port"] = udp_header[0]
                node["udp_dst_port"] = udp_header[1]
                node["udp_data_len"] = udp_header[2]
                node["udp_csum"] = udp_header[3]

                node["data_type"] = UDP
                uh = node["udp_header_size"]
                node["full_offset"] = eh + ih + uh
                node["udp_data_size"] = len(packet) - node["udp_header_size"]
                log.info(("UDP Data size={} th1={} th2={} "
                          "offset={} value={}")
                         .format(node["udp_data_size"],
                                 node["ip_hdr_len"],
                                 node["udp_header_size"],
                                 node["full_offset"],
                                 udp_data))
                err = "failed_udp_data_offset"
                udp_data = packet[node["full_offset"]:]
                target_data = udp_data
                node["error"] = ""
                node["status"] = VALID
            elif node["ip_protocol"] == ICMP_PROTO_IP:

                # unpack the ICMP packet
                packet_min = node["eth_length"] + node["ip_hdr_len"]
                packet_max = packet_min + 4

                log.info(("unpacking ICMP[{}:{}]")
                         .format(packet_min,
                                 packet_max))

                err = ("failed_parsing_ICMP[{}:{}]").format(
                        packet_min,
                        packet_max)

                icmp_datagram = packet[packet_min:packet_max]

                log.info(("unpacking ICMP Header={}")
                         .format(icmp_datagram))

                icmp_header = unpack(ICMP_HEADER_FORMAT, icmp_datagram)

                node["icmp_header_size"] = SIZE_ICMP_HEADER

                node["icmp_type"] = icmp_header[0]
                node["icmp_code"] = icmp_header[1]
                node["icmp_csum"] = icmp_header[2]

                node["data_type"] = ICMP
                ah = node["icmp_header_size"]
                node["full_offset"] = eh + ih + ah
                node["icmp_data_size"] = len(packet) - node["icmp_header_size"]
                log.info(("ICMP Data size={} th1={} th2={} "
                          "offset={} value={}")
                         .format(node["icmp_data_size"],
                                 node["ip_hdr_len"],
                                 node["icmp_header_size"],
                                 node["full_offset"],
                                 icmp_data))
                err = "failed_icmp_data_offset"
                icmp_data = packet[node["full_offset"]:]
                target_data = icmp_data
                node["error"] = ""
                node["status"] = VALID
            else:
                node["error"] = ("unsupported_ip_protocol={}").format(
                                    node["ip_protocol"])
                node["status"] = IP_UNSUPPORTED
            # end of parsing supported protocols the final node data

            if node["status"] == VALID:

                log.debug("filtering")
                # filter out delimiters in the last 64 bytes
                if filter_keys:
                    err = "filtering={}".format(len(filter_keys))
                    log.debug(err)
                    for f in filter_keys:
                        if target_data:
                            if str(f) in str(target_data):
                                log.info(("FOUND filter={} "
                                         "in data={}")
                                         .format(f,
                                                 target_data))
                                node["error"] = "filtered"
                                node["status"] = FILTERED
                                node["filtered"] = f
                                break
                    # end of tagging packets to filter out of the
                    # network-pipe stream
                # if there are filters

                log.debug(("was filtered={}")
                          .format(node["filtered"]))

                if not node["filtered"]:
                    err = "building_stream"
                    log.debug(("building stream target={}")
                              .format(target_data))
                    stream_size = 0
                    if target_data:
                        try:
                            # convert to hex string
                            err = ("concerting target_data to "
                                   "hex string")
                            node["target_data"] = target_data.hex()
                        except Exception as e:
                            log.info(("failed converting={} to "
                                      "utf-8 ex={}")
                                     .format(target_data,
                                             e))
                            err = "str target_data"
                            node["target_data"] = target_data
                        # end of try/ex
                        stream_size += len(node["target_data"])
                    # end of target_data
                    log.debug(("serializing stream={}")
                              .format(node["target_data"]))
                    node_json = json.dumps(node)
                    data_stream = str("{} {}").format(node_json,
                                                      include_filter_key)
                    log.debug("compressing")

                    if stream_size:
                        node["stream"] = data_stream
                # end of building the stream

                log.debug("valid")
            else:
                log.error(("unsupported ip frame ip_protocol={}")
                          .format(node["ip_protocol"]))
            # end of supported IP packet protocol or not
        elif node["eth_protocol"] == ARP_PROTO_ETH:

            arp_packet_min = SIZE_ETH_HEADER
            arp_packet_max = SIZE_ETH_HEADER + 28

            log.info(("unpacking ARP[{}:{}]")
                     .format(arp_packet_min,
                             arp_packet_max))

            err = ("failed_parsing_ARP[{}:{}]").format(
                    arp_packet_min,
                    arp_packet_max)

            # take the first 28 characters for the ARP header
            arp_datagram = packet[arp_packet_min:arp_packet_max]

            arp_header = unpack(ARP_HEADER_FORMAT, arp_datagram)
            # https://docs.python.org/2/library/struct.html#format-characters

            node["arp_header_size"] = SIZE_ARP_HEADER
            node["arp_hw_type"] = arp_header[0].hex()
            node["arp_proto_type"] = arp_header[1].hex()
            node["arp_hw_size"] = arp_header[2].hex()
            node["arp_proto_size"] = arp_header[3].hex()
            node["arp_opcode"] = arp_header[4].hex()
            node["arp_src_mac"] = arp_header[5].hex()
            node["arp_src_ip"] = socket.inet_ntoa(arp_header[6])
            node["arp_dst_mac"] = arp_header[7].hex()
            node["arp_dst_ip"] = socket.inet_ntoa(arp_header[8])

            arp_data = ""
            node["arp_data"] = arp_data
            node["target_data"] = arp_data
            node["data_type"] = ARP
            node["status"] = VALID
            node["arp_data_size"] = len(packet) - node["arp_header_size"]
            node_json = json.dumps(node)
            data_stream = str("{} {}").format(node_json,
                                              include_filter_key)
            node["stream"] = data_stream
        else:
            node["error"] = ("unsupported eth_frame protocol={}").format(
                                node["eth_protocol"])
            node["status"] = ETH_UNSUPPORTED
            log.error(node["error"])
        # end of supported ETH packet or not

    except Exception as e:
        node["status"] = ERROR
        node["error"] = "err={} failed parsing frame ex={}".format(err,
                                                                   e)
        log.error(node["error"])
    # end of try/ex

    return node
# end of parse_network_data
