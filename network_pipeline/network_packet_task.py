import datetime


class NetworkPacketTask(object):
    """NetworkPacketTask"""

    def __init__(self,
                 source="locahost",
                 payload=None):
        """__init__

        :param source:
        :param payload:
        """

        self.source = source
        self.payload = payload
        self.created = datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")

    def __call__(self):
        """__call__"""
        return "{}-{}".format(self.source,
                              self.payload)

    def __str__(self):
        """__str__"""
        return str(("{}-{}")
                   .format(self.source,
                           self.payload))
# end of NetworkPacketTask
