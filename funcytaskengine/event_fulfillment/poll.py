import gevent
import logging

from funcytaskengine.event_fulfillment.return_values import EventSuccessDecoratorResult
from .base import BaseFulfillment


logger = logging.getLogger(__name__)


class PollerFulfillment(BaseFulfillment):

    def __init__(self, type, frequency_ms):
        self.running = False
        self.interval = 1000 / frequency_ms

    def run(self, initiator, conditions, **kwargs):
        """
        Decorates an initiator function and runs it in a loop?

        :param initiator_fn:
        :return:
        """
        self.running = True

        # runs the initiator with a small timeout until the condition is met
        # when all conditions are true it returns
        while self.running:
            logger.debug('%s', {
                'message': 'running poller loop'
            })

            # need to asynchronously schedule initiator and poll for the result so that
            # we can continually reschedule? Ugh this could get crazy
            # how do we handle long connections?

            # should this be synchronous? I think maybe
            initiator_result = initiator.execute()
            conditions.initialize(initiator_result.values())

            # If the initiator does not complete in the interval what happens?
            # should it be killed?? and retried?
            if conditions.are_met():
                logger.debug('%s', {
                    'message': 'poller condition met'
                })
                return EventSuccessDecoratorResult(
                    conditions.values()
                )

            # if the initiator yields will it yield to the calling function?
            # might have to execute it in a greenlet? Ugh, confusing
            gevent.sleep(self.interval)

            # failure is caught by global timeout....


