

class HTTPStatusCodeCondition(object):

    def __init__(self, type, status_code):
        self.status_code = status_code

    def __str__(self):
        return str(self.__dict__)

    def is_met(self, http_response):
        return http_response.status_code == self.status_code