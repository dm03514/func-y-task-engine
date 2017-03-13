import requests


class HTTPInitiator(object):

    def __init__(self, method, type, url):
        self.method = method
        self.url = url

    def execute(self):
        return getattr(requests, self.method)(self.url)
