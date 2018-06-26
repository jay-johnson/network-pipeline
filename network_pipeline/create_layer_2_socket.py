import socket
from spylunking.log.setup_logging import console_logger


log = console_logger(
    name='create_l2_socket')


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
