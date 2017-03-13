from .base import BaseTransitionCondition


class NoopCondition(BaseTransitionCondition):

    def is_met(self, *args, **kwargs):
        return True
