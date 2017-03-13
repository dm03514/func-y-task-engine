from funcytestengine.parsers.loaders import DynamicConfigLoader


class TransitionConditionFactory(DynamicConfigLoader):
    CONFIG_PACKAGE_PATH = __name__


class TransitionConditions(object):

    def __init__(self, config_conditions):
        self.conditions = [
            TransitionConditionFactory.build(cc) for cc in config_conditions
        ]
