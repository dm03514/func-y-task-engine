import logging
import subprocess

from funcytaskengine.event_fulfillment.return_values import EventSuccessDecoratorResult, EventFailureResult
from funcytaskengine.initiators.base import BaseInitiator


logger = logging.getLogger(__name__)


class SubprocessInitiator(BaseInitiator):

    def __init__(self, type, command, arguments):
        self.command = command
        self.arguments = arguments

    def execute(self):
        logger.debug({
            'message': 'executing_command',
            'command': self.command,
            'argumens': self.arguments,
        })
        p = subprocess.Popen([self.command] + self.arguments)
        returncode = p.wait()
        if returncode == 0:
            return EventSuccessDecoratorResult(returncode)

        return EventFailureResult()
