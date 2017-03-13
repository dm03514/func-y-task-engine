from .base import BaseFulfillment


class SingleFireFulfillment(BaseFulfillment):

    def run(self, initiator, conditions):
        return conditions.are_met(initiator.execute())
