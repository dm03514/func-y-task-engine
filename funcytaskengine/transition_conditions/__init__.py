import functools

from funcytaskengine.event_fulfillment.return_values import Valuesable, EventSuccessDecoratorResult
from funcytaskengine.parsers.loaders import DynamicConfigLoader
from funcytaskengine.transition_conditions.exceptions import ConditionNotMet


class TransitionConditionFactory(DynamicConfigLoader):
    CONFIG_PACKAGE_PATH = __name__


class ApplyConditions(object):
    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(self, initiator, conditions, *args, **kwargs):
            result = fn(self, initiator, conditions, *args, **kwargs)
            assert isinstance(result, Valuesable)
            conditions.initialize(result)
            conditions.apply()
            return EventSuccessDecoratorResult(conditions)
        return decorated


class TransitionConditions(object):

    def __init__(self, config_conditions):
        self.conditions = [
            TransitionConditionFactory.build(cc) for cc in config_conditions
        ]
        self.intialized = False
        self.vs = None

    def initialize(self, vs):
        """

        :param vs:
        :return:
        """
        self.initialized = True
        self.vs = vs

    def values(self):
        return self.vs.values()

    def apply(self):
        """
        Checks to see if all the conditions have been met, against the values.

        Mutates the values with the return value of each condition being applied.
        Allows for a transformation, so that the values can be used for other
        event states.

        :return: boolean
        """
        assert self.initialized

        for con in self.conditions:
            self.vs = con.apply(self.vs)

        return True
