import unittest
import yaml

from funcytestengine.machine import TestMachine, STATES


class HTTPSingleStateTestCase(unittest.TestCase):

    def test_single_http_state_success(self):
        """
        Tests that a basic test definition using HTTP
        can be executed successfully.
        """
        HTTP_TEST = """
---
events:
  - name: google_request
    event_fulfillment_strategy:
       type: poll.PollerFulfillment
       frequency_ms: 200
    transition_conditions:
      - type: http.HTTPCondition
        status_code: 200
    initiator:
      method: GET
      type: http.HTTPInitiator
      url: "http://google.com"
max_timeout: 240000
name: single_http_request_test
version: "1"
        """
        state_dict = yaml.load(HTTP_TEST)
        machine = TestMachine(machine_dict=state_dict)
        self.assertEqual(machine.state, STATES.PENDING)
