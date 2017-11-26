import gnsq
import logging

from funcytaskengine.event_fulfillment.return_values import ValuesContainer, EventSuccessDecoratorResult
from funcytaskengine.transition_conditions import ApplyConditions
from .base import BaseFulfillment


logger = logging.getLogger(__name__)


class NSQStreamingFulfillment(BaseFulfillment):

    def __init__(self, type, topic, channel, address, take_n=1, take_time=None):
        self.topic = topic
        self.channel = channel
        self.address = address
        self.take_n = take_n

    @ApplyConditions()
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
        reader._funcy_messages = []
        reader._funcy_take_n = self.take_n

        @reader.on_message.connect
        def handler(_r, message):
            # each message finish and save it
            message.finish()
            _r._funcy_messages.append(message)

            if len(_r._funcy_messages) == self.take_n:
                _r.close()

        reader.start()

        logger.debug({
            'class': self.__class__.__name__,
            'num_messages': len(reader._funcy_messages),
        })

        return ValuesContainer(
            reader._funcy_messages
        )
