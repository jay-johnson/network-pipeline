from network_pipeline.consts import SOURCE
from network_pipeline.consts import FORWARD_BROKER_URL
from network_pipeline.consts import FORWARD_SSL_OPTIONS
from network_pipeline.consts import FORWARD_ENDPOINT_TYPE
from spylunking.log.setup_logging import console_logger
from celery_connectors.publisher import Publisher


log = console_logger(
    name='get_publisher')


def get_publisher():
    """get_publisher"""
    log.info("initializing publisher")
    pub = None
    auth_url = ""
    if FORWARD_ENDPOINT_TYPE == "redis":
        auth_url = FORWARD_BROKER_URL
    else:
        auth_url = FORWARD_BROKER_URL

    pub = Publisher(name="{}_{}".format(SOURCE, "-redis"),
                    auth_url=auth_url,
                    ssl_options=FORWARD_SSL_OPTIONS)

    log.info("publisher={}".format(pub))
    return pub
# end of get_publisher


pub = get_publisher()
