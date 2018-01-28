import logging
import socket
from network_pipeline.log.setup_logging import setup_logging

setup_logging()
name = "create-layer2"
log = logging.getLogger(name)


def create_layer_2_socket():
    """create_layer_2_socket"""

    # create a socket for recording layer 2, 3 and 4 frames
    s = None
    try:
        log.info("Creating l234 socket")
        s = socket.socket(socket.AF_PACKET,
                          socket.SOCK_RAW,
                          socket.ntohs(0x0003))
    except socket.error as msg:
        log.error(("Socket could not be created ex={}")
                  .format(msg))
    return s
# end of create_layer_2_socket
