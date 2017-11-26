from funcytaskengine.event_fulfillment.base import BaseFulfillment
from funcytaskengine.transition_conditions import ApplyConditions


class FromEventNameFulfillment(BaseFulfillment):

    def __init__(self, type, event_name):
        self.event_name = event_name

    @ApplyConditions()
    def run(self, initiator, conditions, event_results, **kwargs):
        return event_results.return_value_from_name(self.event_name)

