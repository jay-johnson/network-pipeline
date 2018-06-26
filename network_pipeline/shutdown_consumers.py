

def shutdown_consumers(num_workers=2,
                       tasks=None,
                       shutdown_msg="SHUTDOWN"):
    """shutdown_consumers

    :param num_workers:
    :param tasks:
    :param shutdown_msg:
    """
    if tasks:
        # Add a poison pill for each consumer
        for i in range(num_workers):
            tasks.put(shutdown_msg)
# end of shutdown_consumers
