import requests

from funcytaskengine.event_fulfillment.return_values import Valuesable
from funcytaskengine.initiators.base import BaseInitiator


class HTTPValues(Valuesable):

    def __init__(self, response):
        self.vs = [response]

    def values(self):
        return self.vs


class HTTPInitiator(BaseInitiator):

    def __init__(self, method, type, url):
        self.method = method
        self.url = url

    def execute(self):
        return HTTPValues(
            getattr(requests, self.method)(self.url)
        )
