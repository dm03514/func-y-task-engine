from funcytestengine.initiators.base import BaseInitiator


class NoopInitiator(BaseInitiator):

    def __init__(self, *args, **kwargs):
        pass

    def execute(self):
        pass
