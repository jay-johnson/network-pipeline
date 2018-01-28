import datetime


class NetworkPacketTask(object):

    def __init__(self,
                 source="locahost",
                 payload=None):

        self.source = source
        self.payload = payload
        self.created = datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")

    def __call__(self):
        return "{}-{}".format(self.source,
                              self.payload)

    def __str__(self):
        return str(("{}-{}")
                   .format(self.source,
                           self.payload))
# end of NetworkPacketTask
