import re
from abc import ABCMeta, abstractproperty, abstractmethod


class BaseTemplateProcessor(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.matcher = re.compile(self.VARIABLE_REGEX)

    @abstractproperty
    def VARIABLE_REGEX(self):
        return None

    @abstractmethod
    def substitute_value(self, template_str, match):
        pass

    def variables(self, template_str):
        """

        :param regex:
        :return:
        """
        match = self.matcher.search(template_str)
        if match:
            return [match]

        return []

    def substitute(self, template_str):

        for match in self.variables(template_str):
            template_str = self.substitute_value(template_str, match)

        return template_str

