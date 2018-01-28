import logging
import multiprocessing
from network_pipeline.log.setup_logging import setup_logging

setup_logging()
name = "start-consumers"
log = logging.getLogger(name)


def start_consumers_for_queue(prefix_name="worker",
                              num_workers=2,
                              tasks=None,
                              queue_to_consume=None,
                              shutdown_msg="SHUTDOWN",
                              consumer_class=None,
                              need_response=False,
                              callback=None):

    consumers = []

    if not consumer_class:
        log.error("Please provide a consumer_class arg")
        log.error("  like: network_pipeline.packet_consumer.PacketConsumer")
        return consumers

    if not tasks:
        log.error("Missing tasks")
        return consumers

    if not queue_to_consume:
        log.error("Missing queue")
        return consumers

    # Establish communication queues
    log.info(("Creating consumers={} for cores={}")
             .format(multiprocessing.cpu_count(),
                     num_workers))

    for i in range(num_workers):
        consumers.append(consumer_class(
                            "{}-{}".format(prefix_name,
                                           i + 1),
                            tasks,
                            queue_to_consume,
                            shutdown_msg=shutdown_msg,
                            need_response=need_response,
                            callback=callback))

    log.info("Starting consumers={}".format(len(consumers)))
    for w in consumers:
        w.start()

    return consumers
# end of start_consumers_for_queue
