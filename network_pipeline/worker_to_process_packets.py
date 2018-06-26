import multiprocessing
from spylunking.log.setup_logging import console_logger


log = console_logger(
    name='worker_to_process_packets')


class WorkerToProcessPackets(multiprocessing.Process):

    def __init__(self,
                 name,
                 task_queue,
                 result_queue,
                 shutdown_msg="SHUTDOWN",
                 need_response=False,
                 callback=None):
        """__init__

        :param name: name of the consumer
        :param task_queue: queue for tasks to process
        :param result_queue: send results to back here
        :param shutdown_msg: custom poison pill  shutdown msg
        :param need_response: send a response back on result_queue
        :param callback: method for processing packets
        """
        multiprocessing.Process.__init__(self)
        self.name = name
        self.response_name = 'pcktr'
        self.task_queue = task_queue
        self.need_response = need_response
        self.result_queue = result_queue

        self.callback = callback
        self.shutdown_msg = shutdown_msg
    # end of __init__

    def run(self):
        """run"""
        if self.callback:
            log.info(("{} - using callback={}")
                     .format(self.name,
                             self.callback))
            self.callback(name=self.response_name,
                          task_queue=self.task_queue,
                          result_queue=self.result_queue,
                          shutdown_msg=self.shutdown_msg)
        else:

            log.info("did not find a callback method "
                     "using - using default handler")

            proc_name = self.name
            while True:
                next_task = self.task_queue.get()
                if next_task:
                    if str(next_task) == self.shutdown_msg:
                        # Poison pill means shutdown
                        log.info(("{}: Exiting msg={}")
                                 .format(self.name,
                                         next_task))
                        self.task_queue.task_done()
                        break
                log.info(("Consumer: {} {}")
                         .format(proc_name, next_task))
                self.task_queue.task_done()

                if self.need_response:
                    answer = "processed: {}".format(next_task())
                    self.result_queue.put(answer)
        # end of if custome callback handler or not

        return
    # end of run

# end of WorkerToProcessPackets
