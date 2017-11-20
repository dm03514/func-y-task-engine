import unittest

from mock import MagicMock

from funcytaskengine.event_fulfillment.return_values import EmptyValues, ValuesCollection, ValuesWrappedContainer
from funcytaskengine.transition_conditions.transformations import ParseJSON


class ParseJSONTestCase(unittest.TestCase):

    def test_no_values(self):
        t = ParseJSON(type=None)
        self.assertEqual(
            EmptyValues().values(),
            t.is_met(EmptyValues()).values(),
        )

    def test_one_valid_value(self):
        t = ParseJSON(type=None)
        self.assertEqual(
            (
                {
                    'hi': 'there',
                },
            ),

            t.is_met(
                ValuesWrappedContainer('{"hi":"there"}')
            ).values()
        )

    def test_many_valid_values(self):
        t = ParseJSON(type=None, value_property='body')
        self.assertEqual(
            (
                {
                    'hi': 'there',
                },
                {
                    'hi1': 'there1',
                }
            ),
            t.is_met(
                ValuesCollection([
                    MagicMock(
                        body='{"hi":"there"}'
                    ),
                    MagicMock(
                        body='{"hi1":"there1"}'
                    ),
                ])
            ).values()
        )
