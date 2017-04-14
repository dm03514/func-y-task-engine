from funcytaskengine.parsers.loaders import DynamicConfigLoader


class InitiatorFactory(DynamicConfigLoader):
    CONFIG_PACKAGE_PATH = __name__

