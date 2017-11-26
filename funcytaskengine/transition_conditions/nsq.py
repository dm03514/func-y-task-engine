import json

import logging

from .base import BaseTransitionCondition


logger = logging.getLogger(__name__)


class NSQOnMessage(BaseTransitionCondition):

    def __init__(self, *args, **kwargs):
        pass

    def apply(self, messages):
        """
        Qualifies whenever any truthy message is received.

        :param message:
        :return: boolean
        """
        if messages:
            logging.debug({
                'messages': messages
            })
            return messages
