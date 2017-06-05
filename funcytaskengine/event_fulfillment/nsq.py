import gnsq
from .base import BaseFulfillment


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

        @reader.on_message.connect
        def handler(_r, message):

            message.finish()

            if conditions.are_met(message):
                _r.close()

        reader.start()


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

        @reader.on_message.connect
        def handler(_r, message):
            message.finish()
            _r.close()
            _r.funcy_message = message

        reader.start()
        return conditions.are_met(reader.funcy_message)
