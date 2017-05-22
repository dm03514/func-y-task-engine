import json

from .base import BaseTransitionCondition


class LengthEqual(BaseTransitionCondition):

    def __init__(self, type, length):
        self.length = length

    def is_met(self, collection):
        assert len(collection) == self.length, 'collection ({}) != expected ({})'.format(
            len(collection), self.length
        )


class ParseJSON(BaseTransitionCondition):

    def is_met(self, value):
        return json.loads(value)
