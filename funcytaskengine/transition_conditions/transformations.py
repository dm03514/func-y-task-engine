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
