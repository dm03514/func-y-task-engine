import gevent
import logging


logger = logging.getLogger(__name__)


class PollerFulfillment(object):

    def __init__(self, type, frequency_ms):
        self.running = False
        self.interval = 1000 / frequency_ms

    def run(self, initiator, conditions):
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

            # If the initiator does not complete in the interval what happens?
            # should it be killed?? and retried?
            if conditions.are_met(initiator.execute()):
                logger.debug('%s', {
                    'message': 'poller condition met'
                })
                return

            # if the initiator yields will it yield to the calling function?
            # might have to execute it in a greenlet? Ugh, confusing
            gevent.sleep(self.interval)


