from .base import BaseTransitionCondition


class NSQOnMessage(BaseTransitionCondition):

    def __init__(self, *args, **kwargs):
        pass

    def is_met(self, message):
        """
        Qualifies whenever any truthy message is received.

        :param message:
        :return: boolean
        """
        if message:
            return message.body
