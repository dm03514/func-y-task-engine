import logging
import subprocess

from funcytaskengine.event_fulfillment.return_values import ValuesContainer
from funcytaskengine.initiators.base import BaseInitiator


logger = logging.getLogger(__name__)


class SubprocessInitiator(BaseInitiator):

    def __init__(self, type, command):
        self.command = command

    def execute(self):
        logger.debug({
            'message': 'executing_command',
            'command': self.command,
        })

        p = subprocess.Popen(self.command)
        returncode = p.wait()
        return ValuesContainer(returncode)
