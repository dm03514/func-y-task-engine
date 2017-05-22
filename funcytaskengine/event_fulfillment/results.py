from funcytaskengine.event_fulfillment.base import BaseFulfillment


class FromEventNameFulfillment(BaseFulfillment):

    def __init__(self, type, event_name):
        self.event_name = event_name

    def run(self, initiator, conditions, **kwargs):
        print('HEEEEEEEEEEEEEEEEEEEEERE')
        print(kwargs)
        conditions.are_met()

