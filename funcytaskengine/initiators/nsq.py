import json

import gnsq
import logging

from funcytaskengine.event_fulfillment.return_values import ValuesWrappedContainer
from .base import BaseInitiator


logger = logging.getLogger(__name__)


class NSQPublisherInitiator(BaseInitiator):

    def __init__(self, type, message, nsqd_address, topic):
        self.message = self.validate_message(message)
        self.nsqd_address = nsqd_address
        self.topic = topic

    def validate_message(self, message):
        return json.loads(message.replace('\n', ''))

    def execute(self):
        logger.debug('%s', {
            'message': 'publishing_message_nsq',
            'body': self.message,
        })

        return ValuesWrappedContainer(
            gnsq.Nsqd(address=self.nsqd_address).publish(
                self.topic,
                json.dumps(self.message)
            )
        )


