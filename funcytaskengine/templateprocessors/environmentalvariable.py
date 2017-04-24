import os

from funcytaskengine.templateprocessors.base import BaseTemplateProcessor


class EnvironmentalVariableTemplateProcessor(BaseTemplateProcessor):
    VARIABLE_REGEX = r'\$ENV_VAR_(?P<variablename>\w+)'

    def substitute_value(self, template_str, match):
        """
        Pulls the variable from the environment.
        TODO - parse it to python type, envparse??

        :param template_str:
        :param match: regex Match object
        :return:
        :raises: KeyError and fails loudly
        """
        template_variable_to_replace = match.group(0)
        env_var = match.group('variablename')
        replaced_template = template_str.replace(
            template_variable_to_replace,
            os.environ[env_var]
        )
        return replaced_template

