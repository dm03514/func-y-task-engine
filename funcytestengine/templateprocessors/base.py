from abc import ABCMeta, abstractproperty, abstractmethod


class BaseTemplateProcessor(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def VARIABLE_REGEX(self):
        return None

    @abstractmethod
    def generate_value(self):
        pass

    def variables(self, regex):
        """

        :param regex:
        :return:
        """
        pass

    def substitute(self, template_str):
        # get all variables which needs substituting

        for variable in self.variables(self.VARIABLE_REGEX):
            template_str = template_str.replace(variable, self.variable_value())

        return template_str

