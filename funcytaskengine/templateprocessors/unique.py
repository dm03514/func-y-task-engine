import uuid

from funcytaskengine.templateprocessors.base import BaseTemplateProcessor


class UUIDStringTemplateProcessor(BaseTemplateProcessor):
    VARIABLE_REGEX = r'\$UUID_STRING_(?P<variablename>\w+)'

    def generate_value(self):
        return uuid.uuid4().get_hex()
