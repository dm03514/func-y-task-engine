import logging

from funcytaskengine.transition_conditions import ApplyConditions
from .base import BaseFulfillment


logger = logging.getLogger(__name__)


class SingleFireFulfillment(BaseFulfillment):

    @ApplyConditions()
    def run(self, initiator, conditions, **kwargs):
        logger.debug({
            'initiator': initiator,
            'conditions': conditions,
        })
        return initiator.execute()

