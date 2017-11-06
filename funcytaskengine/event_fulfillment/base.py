from abc import ABCMeta, abstractmethod


class BaseFulfillment(object):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self, initiator, conditions, **kwargs):
        pass
