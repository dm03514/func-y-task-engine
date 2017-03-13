

class LengthEqual(object):

    def __init__(self, type, length):
        self.length = length

    def is_met(self, collection):
        return len(collection) == self.length