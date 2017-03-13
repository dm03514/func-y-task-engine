import unittest
import yaml

from funcytestengine.machine import TestMachine


class MultiStateTestCase(unittest.TestCase):

    def test_multi_state_nsq_http(self):
        TEST = """
---
events:

  - name: publish_message
    initiator:
      type: NSQ
      message: >
      {
            "attempts": 1,
            "backtrace": [],
            "worker": "PerformRaisesExceptionConsumer",
            "topic": "test",
            "host": "vagrant-ubuntu-trusty-64",
            "process_id": 31616,
            "payload": "testpayloadstring",
            "exception": "Exception", "log": [],
            "error_message": "Exception: ",
            "retrying": True,
            "channel": unique_test_channel_1
      }

  - name: message_processed
    initiator:
      type: NSQ_Reader
      topic: test_topic
      channel: test
      host_port: localhost:4150
    transition_condition:
       type: on_message

  - name: assert_message_in_postgres
    initiator:
        type: postgres
        query: "SELECT COUNT(*) FROM failed_jobs WHERE channel='unique_test_channel_1'"
        username: vagrant
        host: localhost
    event_fulfillment_strategy:
       type: count
       equal: 1
       # instead of polling make a single assertion,
       # as soon as this is executed
       assertion: True

max_timeout: 10000
name: NSQ_async_reader_postgres_assertion
version: "1"
        """
        state_dict = yaml.load(TEST)
        machine = TestMachine(machine_dict=state_dict)
        # import ipdb; ipdb.set_trace();

