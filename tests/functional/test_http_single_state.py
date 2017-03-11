import unittest
import yaml


class HTTPSingleStateTestCase(unittest.TestCase):

    def test_single_http_state_success(self):
        """
        Tests that a basic test definition using HTTP
        can be executed successfully.
        """
        HTTP_TEST = """
---
events:
  google_request:
    event_fulfillment_strategy:
       type: poll
       frequency_ms: 200
    transition_condition:
      type: HTTP
      status_code: 200
    initiator:
      method: GET
      type: HTTP
      url: "http://google.com"
max_timeout: 240000
name: single_http_request_test
version: "1"
        """
        parsed_yaml = yaml.load(HTTP_TEST)
        import ipdb; ipdb.set_trace();
