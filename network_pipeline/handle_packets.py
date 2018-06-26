from network_pipeline.consts import SOURCE
from network_pipeline.consts import FORWARD_EXCHANGE
from network_pipeline.consts import FORWARD_ROUTING_KEY
from network_pipeline.consts import FORWARD_QUEUE
from spylunking.log.setup_logging import console_logger
from network_pipeline.utils import rnow
from network_pipeline.convert_pkt_to_json import convert_pkt_to_json
from network_pipeline.publisher import pub
import scapy.all as scapy


log = console_logger(
    name='proc')


def handle_packets(pk):
    """handle_packets

    :param pk: data packet that scapy sends in
    """

    log.info(("processing with pub={}")
             .format(pub))

    # get the lowest layer
    eth = pk.getlayer(scapy.Ether)

    should_forward = False
    send_msg = {"data": {},
                "created": rnow(),
                "source": SOURCE}

    if eth:
        # parse all layer frames under ethernet
        send_msg["data"] = convert_pkt_to_json(eth)
        should_forward = True
    else:
        log.error(("unsupported pk={}")
                  .format(pk))
    # end of if supported

    if should_forward:

        log.info("forwarding")

        # Publish the message:
        msg_sent = pub.publish(body=send_msg,
                               exchange=FORWARD_EXCHANGE,
                               routing_key=FORWARD_ROUTING_KEY,
                               queue=FORWARD_QUEUE,
                               serializer="json",
                               retry=True)

        log.info("done forwarding={}".format(msg_sent))

    # end of should_forward

# end of handle_packets
