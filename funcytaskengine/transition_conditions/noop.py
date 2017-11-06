from .base import BaseTransitionCondition


class NoopCondition(BaseTransitionCondition):

    def is_met(self, values, *args, **kwargs):
        return values
