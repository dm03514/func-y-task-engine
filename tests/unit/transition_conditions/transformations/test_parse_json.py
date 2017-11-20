import unittest

from mock import MagicMock

from funcytaskengine.transition_conditions.transformations import ParseJSON


class ParseJSONTestCase(unittest.TestCase):

    def test_no_values(self):
        t = ParseJSON(type=None)
        EMPTY_LIST = []
        self.assertEqual(EMPTY_LIST, t.is_met(EMPTY_LIST))

    def test_one_valid_value(self):
        t = ParseJSON(type=None)
        self.assertEqual(
            [
                {
                    'hi': 'there',
                }
            ],
            t.is_met([
                '{"hi":"there"}'
            ])
        )

    def test_many_valid_values(self):
        t = ParseJSON(type=None, value_property='body')
        self.assertEqual(
            [
                {
                    'hi': 'there',
                },
                {
                    'hi1': 'there1',
                }
            ],
            t.is_met([
                MagicMock(
                    body='{"hi":"there"}'
                ),
                MagicMock(
                    body='{"hi1":"there1"}'
                ),
            ])
        )
