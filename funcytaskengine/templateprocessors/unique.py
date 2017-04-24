import uuid

from funcytaskengine.templateprocessors.base import BaseTemplateProcessor


class UUIDStringTemplateProcessor(BaseTemplateProcessor):
    VARIABLE_REGEX = r'\$UUID_STRING_(?P<variablename>\w+)'

    def substitute_value(self, template_str, match):
        return template_str.replace(
            match.group(0),
            uuid.uuid4().get_hex()
        )
