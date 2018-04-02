#!/usr/bin/env python

import logging
from celery_connectors.kombu_subscriber import KombuSubscriber
from network_pipeline.consts import FORWARD_BROKER_URL
from network_pipeline.consts import FORWARD_SSL_OPTIONS
from network_pipeline.consts import FORWARD_QUEUE
from network_pipeline.log.setup_logging import setup_logging
from network_pipeline.record_packets_to_csv import RecordPacketsToCSV


setup_logging(config_name="packets-rabbitmq-logging.json")
name = "kombu-rmq-sub"
log = logging.getLogger(name)

log.info("start - {}".format(name))

agg = RecordPacketsToCSV()


def recv_msg(body,
             message):
    """recv_msg

    Handler method - fires when a messages is consumed from
    the ``FORWARD_QUEUE`` queue running in the ``FORWARD_BROKER_URL``
    broker.

    :param body: message body
    :param message: message object can ack, requeue or reject
    """

    log.info(("callback received msg "))

    agg.handle_msg(
        body=body,
        org_message=message)
# end of recv_msg


def consume_network_packet_messages_from_rabbitmq():
    """consume_network_packet_messages_from_rabbitmq

    Setup a ``celery_connectors.KombuSubscriber`` to consume meessages
    from the ``FORWARD_BROKER_URL`` broker in the ``FORWARD_QUEUE``
    queue.
    """

    # end of recv_message
    # Initialize KombuSubscriber
    sub = KombuSubscriber(
        name,
        FORWARD_BROKER_URL,
        FORWARD_SSL_OPTIONS)

    # Now consume:
    seconds_to_consume = 10.0
    heartbeat = 60
    serializer = "application/json"
    queue = FORWARD_QUEUE

    sub.consume(
        callback=recv_msg,
        queue=queue,
        exchange=None,
        routing_key=None,
        serializer=serializer,
        heartbeat=heartbeat,
        time_to_wait=seconds_to_consume)

    log.info("end - {}".format(name))

# end of consume_network_packet_messages_from_rabbitmq


if __name__ == "__main__":
    consume_network_packet_messages_from_rabbitmq()
