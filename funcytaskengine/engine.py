"""
Drives a TestMachine to completion.

Engine needs to be completely generic and agnostic from any
specific request types, response types, protocols, etc,

adding a new initiator or
"""
import gevent
import logging

from gevent import Timeout
from gevent.queue import Queue

from funcytaskengine import settings
from funcytaskengine.machine import STATES, EVENT_RESULT

logger = logging.getLogger(__name__)


class TaskEngine(object):

    def __init__(self, machine):
        self.machine = machine
        self.event_result_q = Queue(maxsize=1)

    def run(self):
        """
        While determined to be running, run loop is:

        - check if total time has been violated
            - if max time has been validated log and put in finished state
        - wait X seconds for next state
        - yield

        :return:
        """
        # apply the first state so we can follow event loop flow
        self.event_result_q.put_nowait(self.machine.events.first_state())

        logger.debug('%s', {
            'message': 'sending_first_state',
            'first_state': self.machine.events.first_state()
        })

        timeout = Timeout(self.machine.max_timeout)
        timeout.start()
        try:

            while self.machine.is_running():
                # how do we support a general overarching timeout
                # and a specific one for the current running event
                try:
                    # we can ignore the next state, this is only used to indicate
                    # when it's time to apply a transition
                    result = self.event_result_q.get()

                except gevent.queue.Empty:
                    logger.debug('%s', {
                        'message': 'queue_empty',
                    })

                else:
                    if result == EVENT_RESULT.FAILURE:
                        logger.debug('%s', {
                            'message': 'task_failure'
                        })
                        return False

                    logger.debug('%s', {
                        'message': 'state_change_requested',
                    })
                    self.machine.events.teardown_current()
                    self.machine.next_state()

                    if self.machine.state == STATES.FINISHED:
                        logger.debug('%s', {
                            'message': 'task_execution_finished',
                            'status': 'SUCCESS',
                        })
                        return True

                    self.machine.run_current_event(event_result_q=self.event_result_q)

        except Timeout:
            logger.error('%s', {
                'message': 'task timeout reached',
                'timeout': self.machine.max_timeout,
                'units': 'seconds'
            })
            return False

        finally:
            timeout.cancel()

        return True


