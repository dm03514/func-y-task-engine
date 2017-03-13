import gnsq


class NSQStreamingFulfillment(object):

    def __init__(self, type, topic, channel, address):
        self.topic = topic
        self.channel = channel
        self.address = address

    def run(self, initiator, conditions):
        """
        Connects to NSQd instance specified by address, and evaluates
        the conditions against every message received.

        :param initiator:
        :param conditions:
        :return:
        """
        # user can still initiate
        initiator.execute()

        reader = gnsq.Reader(self.topic, self.channel, self.address)

        @reader.on_message.connect
        def handler(_r, message):
            if conditions.are_met(message):
                _r.close()

        reader.start()
