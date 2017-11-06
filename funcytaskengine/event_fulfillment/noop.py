import logging

from funcytaskengine.event_fulfillment.return_values import EventFailureResult
from funcytaskengine.event_fulfillment.return_values import EventSuccessDecoratorResult
from .base import BaseFulfillment


logger = logging.getLogger(__name__)


class SingleFireFulfillment(BaseFulfillment):

    def run(self, initiator, conditions, **kwargs):
        logger.debug({
            'initiator': initiator,
            'conditions': conditions,
        })

        initiator_result = initiator.execute()
        conditions.initialize(initiator_result)

        if conditions.are_met():
            return EventSuccessDecoratorResult(conditions.values())

        return EventFailureResult()
