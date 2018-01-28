import time


class SimulatedWorkTask(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)  # pretend to take some time to do the work
        return "{} * {} = {}".format(self.a, self.b, self.a * self.b)

    def __str__(self):
        return str(("{} * {} = {}")
                   .format(self.a,
                           self.b,
                           float(self.a * self.b)))
# end of SimulatedWorkTask
