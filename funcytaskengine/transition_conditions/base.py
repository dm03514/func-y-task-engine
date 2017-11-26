from abc import ABCMeta, abstractmethod


class BaseTransitionCondition(object):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def apply(self):
        pass
