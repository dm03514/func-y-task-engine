import unittest
import yaml

from funcytestengine.engine import TaskEngine
from funcytestengine.machine import TaskMachine, STATES


class MultiStateTestCase(unittest.TestCase):

    def test_multi_state_nsq_http(self):
        TEST = """
---
events:
  - name: publish_message
    initiator:
      type: nsq.NSQPublisherInitiator
      message: >
          {
                "attempts": 1,
                "backtrace": [],
                "worker": "PerformRaisesExceptionConsumer",
                "topic": "test",
                "host": "vagrant-ubuntu-trusty-64",
                "process_id": 31616,
                "payload": "testpayloadstring",
                "exception": "Exception",
                "log": [],
                "error_message": "Exception: ",
                "retrying": true,
                "channel": "unique_test_channel_2"
          }
      nsqd_address: localhost
      topic: test_topic

  - name: message_processed
    initiator:
      type: nsq.NSQReaderInitiator
      topic: status_topic
      channel: test
      host_port: localhost:4150
    transition_conditions:
        - type: nsq.NSQOnMessage

  - name: assert_message_in_postgres
    initiator:
        type: postgres.SelectInitiator
        query: "SELECT * FROM failed_jobs WHERE channel='unique_test_channel_2'"
        connection_string: "dbname=skycutter_development host=localhost user=vagrant"
    transition_conditions:
        - type: assertions.LengthEqual
          length: 1

max_timeout: 10000
name: NSQ_async_reader_postgres_assertion
version: "1"
        """
        state_dict = yaml.load(TEST)
        machine = TaskMachine(machine_dict=state_dict)
        self.assertEqual(machine.state, STATES.PENDING)
        engine = TaskEngine(machine)
        result = engine.run()
        self.assertEqual(result, True)

