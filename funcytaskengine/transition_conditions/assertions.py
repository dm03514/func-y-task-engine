import json

import logging

from .base import BaseTransitionCondition


logger = logging.getLogger(__name__)


class LengthEqual(BaseTransitionCondition):

    def __init__(self, type, length):
        self.length = length

    def is_met(self, collection):
        assert len(collection) == self.length, 'collection ({}) != expected ({})'.format(
            len(collection), self.length
        )


class ParseJSON(BaseTransitionCondition):

    def __init__(self, type, value_property=None):
        self.value_property = value_property

    def is_met(self, value):
        to_load = value
        if self.value_property:
            to_load = getattr(value, self.value_property)
        return json.loads(to_load)


class HasKeys(BaseTransitionCondition):

    def __init__(self, type, value_property=None, keys=()):
        self.keys = keys
        self.value_property = value_property

    def is_met(self, value):
        to_assert = value
        if self.value_property:
            to_assert = getattr(value, self.value_property)

        logger.info({
            'to_assert': to_assert,
            'keys': self.keys,
        })
        assert set(to_assert) == set(self.keys)
        return to_assert
