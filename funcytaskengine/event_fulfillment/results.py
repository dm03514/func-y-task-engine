from funcytaskengine.event_fulfillment.base import BaseFulfillment
from funcytaskengine.event_fulfillment.return_values import EventSuccessDecoratorResult, EventFailureResult


def extract_fn(values):
    return values[0]


class FromEventNameFulfillment(BaseFulfillment):

    def __init__(self, type, event_name):
        self.event_name = event_name

    def run(self, initiator, conditions, event_results, **kwargs):
        result = event_results.return_value_from_name(self.event_name)
        i = extract_fn(result.values())

        conditions.initialize(i)

        if conditions.are_met():
            return EventSuccessDecoratorResult(i)

        return EventFailureResult()

