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
    def generate_value(self):
        pass

    def variables(self, template_str):
        """

        :param regex:
        :return:
        """
        match = self.matcher.search(template_str)
        if match:
            return [match.group(0)]

        return []

    def substitute(self, template_str):
        # get all variables which needs substituting

        for variable in self.variables(template_str):
            template_str = template_str.replace(variable, self.generate_value())

        return template_str

