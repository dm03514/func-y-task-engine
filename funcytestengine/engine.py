"""
Drives a TestMachine to completion.

Engine needs to be completely generic and agnostic from any
specific request types, response types, protocols, etc,

adding a new initiator or
"""
import time

import gevent
from gevent.queue import Queue

from funcytestengine import settings


class TestEngine(object):

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
        while self.machine.is_running():
            # how do we support a general overarching timeout
            # and a specific one for the current running event
            try:
                next_state = self.next_state_q.get(block=False)
            except Queue.Empty:
                pass
            else:
                self.machine.events.teardown_current()
                self.machine.next_state()
                self.machine.run_current_event(next_state_q=self.next_state_q)
            # if the next state has completed continue
            finally:
                gevent.sleep(settings.ENGINE_LOOP_INTERVAL)


