#!/usr/bin/env python

import os
import logging
import multiprocessing
import time
from celery_connectors.utils import ev
from network_pipeline.log.setup_logging import setup_logging
from network_pipeline.tcp_helpers import send_msg
from network_pipeline.consts import VALID
from network_pipeline.consts import INVALID
from network_pipeline.consts import FILTERED
from network_pipeline.consts import TCP
from network_pipeline.consts import UDP
from network_pipeline.consts import ARP
from network_pipeline.consts import ICMP
from network_pipeline.consts import INCLUDED_IGNORE_KEY
from network_pipeline.parse_network_data import \
    parse_network_data
from network_pipeline.worker_to_process_packets import \
    WorkerToProcessPackets
from network_pipeline.start_consumers_for_queue import \
    start_consumers_for_queue
from network_pipeline.shutdown_consumers import shutdown_consumers
from network_pipeline.connect_forwarder import connect_forwarder
from network_pipeline.create_layer_2_socket import create_layer_2_socket
from network_pipeline.network_packet_task import \
    NetworkPacketTask


setup_logging()
# network agent
name = "nta"
log = logging.getLogger(name)


def publish_processed_network_packets(
        name="not-set",
        task_queue=None,
        result_queue=None,
        need_response=False,
        shutdown_msg="SHUTDOWN"):

    """
    # Redis/RabbitMQ/SQS messaging endpoints for pub-sub
    routing_key = ev("PUBLISH_EXCHANGE",
                     "reporting.accounts")
    queue_name = ev("PUBLISH_QUEUE",
                    "reporting.accounts")
    auth_url = ev("PUB_BROKER_URL",
                  "redis://localhost:6379/0")
    serializer = "json"
    """

    # these keys need to be cycled to prevent
    # exploiting static keys
    filter_key = ev("IGNORE_KEY",
                    INCLUDED_IGNORE_KEY)

    forward_host = ev("FORWARD_HOST", "127.0.0.1")
    forward_port = int(ev("FORWARD_PORT", "80"))
    include_filter_key = ev("FILTER_KEY", "")
    if not include_filter_key and filter_key:
        include_filter_key = filter_key

    filter_keys = [filter_key]

    log.info(("START consumer={} "
              "forward={}:{} with "
              "key={} filters={}")
             .format(name,
                     forward_host,
                     forward_port,
                     include_filter_key,
                     filter_key))

    forward_skt = None

    not_done = True
    while not_done:

        if not forward_skt:
            forward_skt = connect_forwarder(
                            forward_host=forward_host,
                            forward_port=forward_port)

        next_task = task_queue.get()
        if next_task:

            if str(next_task) == shutdown_msg:
                # Poison pill for shutting down
                log.info(("{}: DONE CALLBACK "
                          "Exiting msg={}")
                         .format(name,
                                 next_task))
                task_queue.task_done()
                break
            # end of handling shutdown case

            try:
                log.debug(("{} parsing")
                          .format(name))

                source = next_task.source
                packet = next_task.payload

                if not packet:
                    log.error(("{} invalid task found "
                               "{} missing payload")
                              .format(name,
                                      next_task))
                    break

                log.debug(("{} found msg from src={}")
                          .format(name,
                                  source))

                network_data = parse_network_data(
                                  data_packet=packet,
                                  include_filter_key=include_filter_key,
                                  filter_keys=filter_keys)

                if network_data["status"] == VALID:
                    if network_data["data_type"] == TCP \
                        or network_data["data_type"] == UDP \
                            or network_data["data_type"] == ARP \
                            or network_data["data_type"] == ICMP:

                        log.info(("{} valid={} packet={} "
                                  "data={}")
                                 .format(name,
                                         network_data["id"],
                                         network_data["data_type"],
                                         network_data["target_data"]))

                        if not forward_skt:
                            forward_skt = connect_forwarder(
                                            forward_host=forward_host,
                                            forward_port=forward_port)

                        if forward_skt:
                            if network_data["stream"]:

                                sent = False
                                while not sent:
                                    try:
                                        log.info("sending={}".format(
                                            network_data["stream"]))
                                        send_msg(
                                            forward_skt,
                                            network_data["stream"]
                                            .encode("utf-8"))
                                        sent = True
                                    except Exception as e:
                                        sent = False
                                        time.sleep(0.5)
                                        try:
                                            forward_skt.close()
                                            forward_skt = None
                                        except Exception as w:
                                            forward_skt = None
                                        forward_skt = connect_forwarder(
                                            forward_host=forward_host,
                                            forward_port=forward_port)
                                # end of reconnecting

                                log.info("sent={}".format(
                                    network_data["stream"]))

                                if need_response:
                                    log.info("receiving")
                                    cdr_res = forward_skt.recv(1024)
                                    log.info(("cdr - res{}")
                                             .format(cdr_res))
                            else:
                                log.info(("{} EMPTY stream={} "
                                          "error={} status={}")
                                         .format(
                                            name,
                                            network_data["stream"],
                                            network_data["err"],
                                            network_data["status"]))
                    else:
                        log.info(("{} not_supported valid={} "
                                  "packet data_type={} status={}")
                                 .format(name,
                                         network_data["id"],
                                         network_data["data_type"],
                                         network_data["status"]))
                elif network_data["status"] == FILTERED:
                    log.info(("{} filtered={} status={}")
                             .format(name,
                                     network_data["filtered"],
                                     network_data["status"]))
                else:
                    if network_data["status"] == INVALID:
                        log.info(("{} invalid={} packet={} "
                                  "error={} status={}")
                                 .format(name,
                                         network_data["id"],
                                         network_data["data_type"],
                                         network_data["error"],
                                         network_data["status"]))
                    else:
                        log.info(("{} unknown={} packet={} "
                                  "error={} status={}")
                                 .format(name,
                                         network_data["id"],
                                         network_data["data_type"],
                                         network_data["error"],
                                         network_data["status"]))
                # end of if valid or not data
            except KeyboardInterrupt as k:
                log.info(("{} stopping")
                         .format(name))
                break
            except Exception as e:
                log.error(("{} failed packaging packet to forward "
                           "with ex={}")
                          .format(name,
                                  e))
                break
            # end of try/ex during payload processing
        # end of if found a next_task

        log.info(("Consumer: {} {}")
                 .format(name, next_task))
        task_queue.task_done()

        if need_response:
            answer = "processed: {}".format(next_task())
            result_queue.put(answer)
    # end of while

    if forward_skt:
        try:
            forward_skt.close()
            log.info("CLOSED connection")
            forward_skt = None
        except Exception:
            log.info("CLOSED connection")
    # end of cleaning up forwarding socket

    log.info("{} Done".format(name))

    return
# end of publish_processed_network_packets


def run_main(need_response=False,
             callback=None):

    stop_file = ev("STOP_FILE",
                   "/opt/stop_recording")

    num_workers = int(ev("NUM_WORKERS",
                         "1"))
    shutdown_msg = "SHUTDOWN"

    log.info("Start - {}".format(name))

    log.info("Creating multiprocessing queue")
    tasks = multiprocessing.JoinableQueue()
    queue_to_consume = multiprocessing.Queue()
    host = "localhost"

    # Start consumers
    log.info("Starting Consumers to process queued tasks")
    consumers = start_consumers_for_queue(
        num_workers=num_workers,
        tasks=tasks,
        queue_to_consume=queue_to_consume,
        shutdown_msg=shutdown_msg,
        consumer_class=WorkerToProcessPackets,
        callback=callback)

    log.info("creating socket")
    skt = create_layer_2_socket()
    log.info("socket created")

    not_done = True
    while not_done:

        if not skt:
            log.info("Failed to create layer 2 socket")
            log.info("Please make sure to run as root")
            not_done = False
            break

        try:
            if os.path.exists(stop_file):
                log.info(("Detected stop_file={}")
                         .format(stop_file))
                not_done = False
                break
            # stop if the file exists

            # Only works on linux
            packet = skt.recvfrom(65565)

            if os.path.exists(stop_file):
                log.info(("Detected stop_file={}")
                         .format(stop_file))
                not_done = False
                break
            # stop if the file was created during a wait loop

            tasks.put(NetworkPacketTask(source=host,
                                        payload=packet))

        except KeyboardInterrupt as k:
            log.info("Stopping")
            not_done = False
            break
        except Exception as e:
            log.error(("Failed reading socket with ex={}")
                      .format(e))
            not_done = False
            break
        # end of try/ex during socket receving

    # end of while processing network packets

    log.info(("Shutting down consumers={}")
             .format(len(consumers)))

    shutdown_consumers(num_workers=num_workers,
                       tasks=tasks)

    # Wait for all of the tasks to finish
    if need_response:
        log.info("Waiting for tasks to finish")
        tasks.join()

    log.info("Done waiting for tasks to finish")
# end of run_main


if __name__ == "__main__":
    run_main(need_response=False,
             callback=publish_processed_network_packets)
    log.info("ending")
