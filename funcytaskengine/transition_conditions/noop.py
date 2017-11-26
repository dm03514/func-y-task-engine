from .base import BaseTransitionCondition


class NoopCondition(BaseTransitionCondition):

    def apply(self, values, *args, **kwargs):
        return values
