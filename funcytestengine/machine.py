from collections import namedtuple

import gevent
from transitions import Machine

from funcytestengine.event_fulfillment import EventFulfillmentFactory
from funcytestengine.initiators import InitiatorFactory

### This file needs to generically operation on ANY subclasses
from funcytestengine.transition_conditions import TransitionConditions

STATES = namedtuple('States', ['PENDING', 'FINISHED'])('pending', 'finished')


class Event(object):
    def __init__(self,
                 name,
                 transition_conditions,
                 initiator,
                 event_fulfillment_strategy=None):
        self.name = name
        self.initiator = InitiatorFactory.build(initiator)
        self.fulfillment = EventFulfillmentFactory.build(event_fulfillment_strategy)
        self.conditions = TransitionConditions(config_conditions=transition_conditions)


class Events(object):
    def __init__(self, events_list):
        self.events_list = events_list

    def states(self):
        return [e.name for e in self.events_list]

    def first_state(self):
        return self.states()[0]

    def teardown_current(self):
        pass

    def run(self, event_name, next_state_q):
        gevent.sleep(0.5)
        next_state_q.put('next_state')


class TaskMachine(object):

    def __init__(self, machine_dict):
        # self.machine_dict = machine_dict
        self.events = Events([Event(**e) for e in machine_dict['events']])
        self.machine = Machine(
            model=self,
            states=self.states(),
            initial=STATES.PENDING
        )
        self.machine.add_ordered_transitions()

    def states(self):
        pre_states = [STATES.PENDING]
        # scheduled?
        # pre-flight resource checks? if a db or an integration
        # is not accessible, fail early option
        post_states = [STATES.FINISHED]
        return pre_states + self.events.states() + post_states

    def is_running(self):
        return True

    # can event fulfillment strategy decorate?
    # noop strategy by default
    def run_current_event(self, next_state_q):
        """
        Executes the current event, using the provided fulfilment strategy
        until the transition conditions are met.

        TODO, errors, timeouts, etc.

        :param next_state_q:
        :return:
        """
        # right now sleep then trigger completion
        gevent.spawn(self.events.run, self.state, next_state_q)

