import gnsq

from funcytaskengine.event_fulfillment.return_values import EventResult, EventFailureResult
from .base import BaseFulfillment


class NSQResult(EventResult):

    def __init__(self, messages):
        self.messages = messages

    def values(self):
        return self.messages

    def success(self):
        return True


class NSQStreamingFulfillment(BaseFulfillment):

    def __init__(self, type, topic, channel, address):
        self.topic = topic
        self.channel = channel
        self.address = address

    def run(self, initiator, conditions, **kwargs):
        """
        Connects to NSQd instance specified by address, and evaluates
        the conditions against every message received.

        :param initiator:
        :param conditions:
        :return:
        """
        # user can still initiate
        initiator.execute()

        reader = gnsq.Reader(self.topic, self.channel, self.address)
        reader._funcy_conditions = conditions

        @reader.on_message.connect
        def handler(_r, message):
            message.finish()

            _r._funcy_conditions.initialize(message)
            if _r._funcy_conditions.are_met():
                _r.close()

        reader.start()
        return NSQResult(messages=reader._funcy_conditions.values())


# TODO WE SHOULDN"T HAVE A SINGLE MESSAGE FULFILLMENT, WE SHOULD HAVE
# GENERIC OPERATORS THAT CAN TAKE 1, N, or TIME WORTH OF MESSAGES
class NSQStreamingSingleMessageFulfillment(BaseFulfillment):

    def __init__(self, type, topic, channel, address):
        self.topic = topic
        self.channel = channel
        self.address = address

    def run(self, initiator, conditions, **kwargs):
        """
        Connects to NSQd instance specified by address, and evaluates
        the conditions on the first message received.

        :param initiator:
        :param conditions:
        :return:
        """
        # user can still initiate
        initiator.execute()

        reader = gnsq.Reader(self.topic, self.channel, self.address)
        reader._funcy_messages = []

        @reader.on_message.connect
        def handler(_r, message):
            message.finish()
            _r.close()
            _r._funcy_messages.append(message)

        reader.start()

        conditions.initialize(reader._funcy_messages)

        if conditions.are_met():
            return NSQResult(messages=conditions.values())

        return EventFailureResult()
