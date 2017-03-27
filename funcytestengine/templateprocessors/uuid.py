import uuid

from funcytestengine.templateprocessors.base import BaseTemplateProcessor


class UUIDStringTemplateProcessor(BaseTemplateProcessor):
    VARIABLE_REGEX = '$UUID_STRING_'

    def generate_value(self):
        return uuid.uuid4().get_hex()
