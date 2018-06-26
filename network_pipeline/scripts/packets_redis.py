#!/usr/bin/env python

from spylunking.log.setup_logging import console_logger
from celery_connectors.kombu_subscriber import KombuSubscriber
from network_pipeline.consts import FORWARD_BROKER_URL
from network_pipeline.consts import FORWARD_SSL_OPTIONS
from network_pipeline.consts import FORWARD_QUEUE
from network_pipeline.record_packets_to_csv import RecordPacketsToCSV


name = 'packets_redis'
log = console_logger(
    name=name)


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


def consume_network_packet_messages_from_redis():
    """consume_network_packet_messages_from_redis

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
# end of consume_network_packet_messages_from_redis


if __name__ == "__main__":
    consume_network_packet_messages_from_redis()
