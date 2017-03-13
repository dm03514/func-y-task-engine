

class SingleFireFulfillment(object):

    def __init__(self, *args, **kwargs):
        pass

    def run(self, initiator, conditions):
        return conditions.are_met(initiator.execute())
