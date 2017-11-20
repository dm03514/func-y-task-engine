import json
import logging

from funcytaskengine.transition_conditions.base import BaseTransitionCondition


logger = logging.getLogger(__name__)


class DictExtractFields(BaseTransitionCondition):
    def __init__(self, type, fields):
        self.fields = fields

    def is_met(self, values):
        logger.info({
            'class': self.__class__.__name__,
            'values': values,
            'fields_to_extract': self.fields
        })
        extracted = []
        for v in values:
            ex = {}
            for f in self.fields:
                ex[f] = v[f]
            extracted.append(ex)
        return extracted


class ListToDictByKey(BaseTransitionCondition):

    def __init__(self, type, by_key):
        self.by_key = by_key

    def is_met(self, values):
        # what to do if a dictionary has the same key?!?!?
        return {v[self.by_key]: v for v in values}


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
