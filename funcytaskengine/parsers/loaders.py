import importlib

from abc import ABCMeta, abstractproperty


def module_attribute_import(attribute_path):
    """
    Dynamically imports a module property.
    This takes care of importing a module then returning a specifically
    referenced attribute in that module.
    :return:
    """
    path_parts = attribute_path.split('.')
    # remove the last element, representing the attribute
    attribute = path_parts.pop()

    # recreate the path to the module
    module_path = '.'.join(path_parts)

    module = importlib.import_module(module_path)
    return getattr(module, attribute)


class DynamicConfigLoader(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def CONFIG_PACKAGE_PATH(self):
        pass

    @classmethod
    def build(cls, test_config):
        """
        Dynamically loads the class based on the type

        :param type:
        :return:
        """
        DynamicClass = module_attribute_import(
            '.'.join([cls.CONFIG_PACKAGE_PATH, test_config['type']]))
        return DynamicClass(**test_config)
