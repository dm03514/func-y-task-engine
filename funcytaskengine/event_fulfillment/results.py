from funcytaskengine.event_fulfillment.base import BaseFulfillment


class FromEventNameFulfillment(BaseFulfillment):

    def __init__(self, type, event_name):
        self.event_name = event_name

    def run(self, initiator, conditions, **kwargs):
        return_value = kwargs['events'].return_value(self.event_name)
        import ipdb; ipdb.set_trace();
        print('HEEEEEEEEEEEEEEEEEEEEERE')
        print(kwargs)
        conditions.are_met(return_value)

