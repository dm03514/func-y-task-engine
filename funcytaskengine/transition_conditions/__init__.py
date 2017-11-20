from funcytaskengine.parsers.loaders import DynamicConfigLoader


class TransitionConditionFactory(DynamicConfigLoader):
    CONFIG_PACKAGE_PATH = __name__


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

    def are_met(self):
        """
        Checks to see if all the conditions have been met, against the values.

        Mutates the values with the return value of each condition being applied.
        Allows for a transformation, so that the values can be used for other
        event states.

        :return: boolean
        """
        assert self.initialized

        for con in self.conditions:
            self.vs = con.is_met(self.vs)

        return bool(self.vs)
