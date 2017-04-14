from funcytaskengine.parsers.loaders import DynamicConfigLoader


class EventFulfillmentFactory(DynamicConfigLoader):
    CONFIG_PACKAGE_PATH = __name__
