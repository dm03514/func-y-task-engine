

class NoopCondition(object):

    def __init__(self, *args, **kwargs):
        pass

    def is_met(self, *args, **kwargs):
        return True
