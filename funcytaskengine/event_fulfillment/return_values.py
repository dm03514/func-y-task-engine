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


class Valuesable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def values(self):
        raise NotImplementedError()


class EmptyValues(Valuesable):
    def values(self):
        return ()


class ValuesCollection(Valuesable):
    def __init__(self, vs):
        self.vs = tuple(vs)

    def values(self):
        return self.vs


class ValuesWrappedContainer(Valuesable):
    """
    Takes a single value and wraps it in a list so
    it complies with the Valuesable interface.
    """
    def __init__(self, value):
        self.v = value

    def values(self):
        return (self.v,)


class EventFailureResult(EventResult):

    def success(self):
        return False

    def values(self):
        return []
