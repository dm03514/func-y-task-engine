import json

import logging

from nose.tools import assert_dict_equal

from .base import BaseTransitionCondition


logger = logging.getLogger(__name__)


class DictEqual(BaseTransitionCondition):
    def __init__(self, type, members):
        self.members = members

    def is_met(self, values):
        logger.info({
            'class': self.__class__,
            'members': self.members,
        })
        assertion_dict = self._build_dict_from_yml_members(self.members)
        assert_dict_equal(values, assertion_dict, '{} != {}'.format(values, assertion_dict))
        return values

    def _build_dict_from_yml_members(self, yml_members):
        return {
            m['key']: m['values'] for m in yml_members
        }


class LengthEqual(BaseTransitionCondition):

    def __init__(self, type, length):
        self.length = length

    def is_met(self, collection):
        logger.info({
            'class': self.__class__,
            'collection': collection,
            'length': self.length,
        })
        assert len(collection) == self.length, 'collection ({}) != expected ({})'.format(
            len(collection), self.length
        )
        return collection


class ParseJSON(BaseTransitionCondition):

    def __init__(self, type, value_property=None):
        self.value_property = value_property

    def is_met(self, values):
        vs = []
        for v in values:
            vs.append(self.parse(v))
        return vs

    def parse(self, value):
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
            'type': self,
            'to_assert': to_assert,
            'keys': self.keys,
        })
        assert set(to_assert) == set(self.keys)
        return to_assert
