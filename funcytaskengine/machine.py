from collections import namedtuple, OrderedDict

import gevent
import logging

from gevent import Timeout
from transitions import Machine

from funcytaskengine.event_fulfillment import EventFulfillmentFactory
from funcytaskengine.initiators import InitiatorFactory

### This file needs to generically operation on ANY subclasses
from funcytaskengine.transition_conditions import TransitionConditions

STATES = namedtuple('States', ['PENDING', 'FINISHED'])('pending', 'finished')
EVENT_RESULT = namedtuple('EventResult', ['SUCCESS', 'FAILURE'])('success', 'failure')


logger = logging.getLogger(__name__)
FIVE_MINUTES = 60 * 5


class EventResult(object):

    def __init__(self, status, context):
        self.status = status
        self.context = context


class Event(object):
    def __init__(self,
                 name,
                 initiator={'type': 'noop.NoopInitiator'},
                 transition_conditions=[{'type': 'noop.NoopCondition'}],
                 event_fulfillment_strategy={'type': 'noop.SingleFireFulfillment'},
                 timeout=FIVE_MINUTES):
        self.name = name
        self.initiator = InitiatorFactory.build(initiator)
        self.fulfillment = EventFulfillmentFactory.build(event_fulfillment_strategy)
        self.conditions = TransitionConditions(config_conditions=transition_conditions)
        self.timeout = timeout

    def execute(self, **kwargs):
        """
        Runs the fulfillment strategy on the initiator until the conditions are met.

        :return:
        """
        with gevent.Timeout(self.timeout):
            return self.fulfillment.run(self.initiator, self.conditions, **kwargs)


class Events(object):
    def __init__(self, events_list):
        self.events_dict = OrderedDict([(e.name, e) for e in events_list])
        # stores the return value of each of the events
        # not sure how this will be formalized....
        self.event_return_values = {}

    def states(self):
        return self.events_dict.keys()

    def first_state(self):
        return self.states()[0]

    def teardown_current(self):
        pass

    def return_value(self, event_name):
        return self.event_return_values[event_name]

    def run(self, event_name, event_result_q):
        # TODO per event timeout
        # get the current event,
        event = self.events_dict[event_name]

        self.event_return_values[event_name] = None

        try:
            self.event_return_values[event_name] = event.execute(
                events=self
            )
        except (Exception, Timeout) as e:
            logger.error('%s', {
                'message': 'event_execution_error',
                'exception': e,
                'event_name': event_name
            })
            event_result_q.put(EVENT_RESULT.FAILURE)
        else:
            event_result_q.put(EVENT_RESULT.SUCCESS)


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
        self.max_timeout = machine_dict.get('max_timeout', FIVE_MINUTES)

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
    def run_current_event(self, event_result_q):
        """
        Executes the current event, using the provided fulfilment strategy
        until the transition conditions are met.

        TODO, errors, timeouts, etc.

        :param next_state_q:
        :return:
        """
        # right now sleep then trigger completion
        gevent.spawn(self.events.run, self.state, event_result_q)

