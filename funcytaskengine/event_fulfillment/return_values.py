from abc import ABCMeta, abstractmethod


class EventResults(object):
    def __init__(self):
        self.by_event_name = {}
        self.in_order = []

    def add(self, return_value):
        self.in_order.append(return_value)
        self.by_event_name[return_value.event_name] = return_value

    def return_value_from_name(self, event_name):
        return self.by_event_name[event_name]


class EventResult(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def success(self):
        pass

    @abstractmethod
    def values(self):
        pass


class EventSuccessDecoratorResult(EventResult):

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def success(self):
        return True

    def values(self):
        return self.wrapped.values()


class EventFailureResult(EventResult):

    def success(self):
        return False

    def values(self):
        return []
