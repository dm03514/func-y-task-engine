from funcytaskengine.event_fulfillment.base import BaseFulfillment
from funcytaskengine.event_fulfillment.return_values import EventSuccessDecoratorResult, EventFailureResult


class FromEventNameFulfillment(BaseFulfillment):

    def __init__(self, type, event_name):
        self.event_name = event_name

    def run(self, initiator, conditions, event_results, **kwargs):
        result = event_results.return_value_from_name(self.event_name)

        conditions.initialize(result.values())

        if conditions.are_met():
            return EventSuccessDecoratorResult(conditions.values())

        return EventFailureResult()

