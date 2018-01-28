import logging
import socket
import time
from network_pipeline.log.setup_logging import setup_logging

setup_logging()
name = "connect-forwarder"
log = logging.getLogger(name)


def connect_forwarder(forward_host=None,
                      forward_port=None,
                      max_retries=-1,
                      sleep_interval=1.0):
    """connect_forwarder

    :param forward_host: host for receiving forwarded packets
    :param forward_port: port for the forwarded packets
    :param max_retries: retries, -1 = infinite
    :param sleep_interval: how often to retry in this loop
    """

    forward_skt = None
    retry_count = 0
    if max_retries == -1:
        retry_count = -2

    if forward_host and forward_port:
        while not forward_skt and \
              retry_count < max_retries:
            try:
                forward_skt = socket.socket()
                log.info(("connecting to forward={}:{}")
                         .format(forward_host,
                                 forward_port))
                forward_skt.connect((forward_host,
                                     forward_port))
                log.debug(("connected to forward={}:{}")
                          .format(forward_host,
                                  forward_port))
            except Exception as s:
                forward_skt = None
                log.error(("Failed to connect forward address={}:{} "
                           "with ex={}")
                          .format(forward_host,
                                  forward_port,
                                  s))
                if max_retries == -1:
                    retry_count = -2
                else:
                    retry_count += 1
            # end of try/ex
            time.sleep(sleep_interval)
        # end of setting up forward
    # end forward_host and forward_port

    return forward_skt
# end of connect_forwarder
