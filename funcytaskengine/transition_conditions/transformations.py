import json
import logging

from funcytaskengine.event_fulfillment.return_values import ValuesCollection, ValuesWrappedContainer
from funcytaskengine.transition_conditions.base import BaseTransitionCondition


logger = logging.getLogger(__name__)


class DictExtractFields(BaseTransitionCondition):
    def __init__(self, type, fields):
        self.fields = fields

    def is_met(self, vs):
        logger.info({
            'class': self.__class__.__name__,
            'values': vs.values(),
            'fields_to_extract': self.fields
        })
        transformed = []
        for v in vs.values():
            ex = {}
            for f in self.fields:
                ex[f] = v[f]
            transformed.append(ex)
        return ValuesCollection(transformed)


class ListToDictByKey(BaseTransitionCondition):

    def __init__(self, type, by_key):
        self.by_key = by_key

    def is_met(self, vs):
        # what to do if a dictionary has the same key?!?!?
        return ValuesWrappedContainer(
            {v[self.by_key]: v for v in vs.values()}
        )


class ParseJSON(BaseTransitionCondition):

    def __init__(self, type, value_property=None):
        self.value_property = value_property

    def is_met(self, vs):
        transformed = []
        for v in vs.values():
            transformed.append(self.parse(v))
        return ValuesCollection(transformed)

    def parse(self, value):
        to_load = value
        if self.value_property:
            to_load = getattr(value, self.value_property)
        return json.loads(to_load)
