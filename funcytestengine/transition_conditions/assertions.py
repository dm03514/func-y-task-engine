

class LengthEqual(object):

    def __init__(self, type, length):
        self.length = length

    def is_met(self, collection):
        assert len(collection) == self.length, 'collection ({}) != expected ({})'.format(
            len(collection), self.length
        )