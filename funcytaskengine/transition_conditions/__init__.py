from funcytaskengine.parsers.loaders import DynamicConfigLoader


class TransitionConditionFactory(DynamicConfigLoader):
    CONFIG_PACKAGE_PATH = __name__


class TransitionConditions(object):

    def __init__(self, config_conditions):
        self.conditions = [
            TransitionConditionFactory.build(cc) for cc in config_conditions
        ]

    def are_met(self, initiator_result):
        """
        Checks to see if all the conditions have been met.

        :param initiator_result:
        :return: boolean
        """
        return [con.is_met(initiator_result) for con in self.conditions]

