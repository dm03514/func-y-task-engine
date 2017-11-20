import requests

from funcytaskengine.event_fulfillment.return_values import ValuesWrappedSingle
from funcytaskengine.initiators.base import BaseInitiator


class HTTPInitiator(BaseInitiator):

    def __init__(self, method, type, url):
        self.method = method
        self.url = url

    def execute(self):
        return ValuesWrappedSingle(
            getattr(requests, self.method)(self.url)
        )
