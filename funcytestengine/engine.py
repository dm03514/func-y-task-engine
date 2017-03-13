"""
Drives a TestMachine to completion.

Engine needs to be completely generic and agnostic from any
specific request types, response types, protocols, etc,

adding a new initiator or
"""
import time

import gevent
import logging
from gevent.queue import Queue

from funcytestengine import settings
from funcytestengine.machine import STATES


logger = logging.getLogger(__name__)


class TaskEngine(object):

    def __init__(self, machine):
        self.machine = machine
        self.next_state_q = Queue(maxsize=1)

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
        self.next_state_q.put_nowait(self.machine.events.first_state())

        logger.debug('%s', {
            'message': 'sending_first_state',
            'first_state': self.machine.events.first_state()
        })

        # TODO APPLY GLOBAL TIMEOUT

        while self.machine.is_running():
            # how do we support a general overarching timeout
            # and a specific one for the current running event
            try:
                # we can ignore the next state, this is only used to indicate
                # when it's time to apply a transition
                _ = self.next_state_q.get(block=False)

            except gevent.queue.Empty:
                logger.debug('%s', {
                    'message': 'queue_empty',
                })

            else:
                logger.debug('%s', {
                    'message': 'state_change_requested',
                })
                self.machine.events.teardown_current()
                self.machine.next_state()

                if self.machine.state == STATES.FINISHED:
                    logger.debug('%s', {
                        'message': 'task_execution_finished',
                    })
                    break

                self.machine.run_current_event(next_state_q=self.next_state_q)

            gevent.sleep(settings.ENGINE_LOOP_INTERVAL)

        return True


