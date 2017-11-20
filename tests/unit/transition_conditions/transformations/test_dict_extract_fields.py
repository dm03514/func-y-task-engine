import unittest

from funcytaskengine.event_fulfillment.return_values import EmptyValues, ValuesCollection, ValuesWrappedContainer
from funcytaskengine.transition_conditions.transformations import DictExtractFields


class DictExtractFieldsTestCase(unittest.TestCase):

    def test_no_values(self):
        extractor = DictExtractFields(type=None, fields=['test'])
        self.assertEqual(
            EmptyValues().values(),
            extractor.is_met(EmptyValues()).values(),
        )

    def test_single_value(self):
        extractor = DictExtractFields(type=None, fields=['test'])
        values = ValuesWrappedContainer(
            {
                'hi': 'hello',
                'test': 'ok',
            },
        )

        self.assertEqual(
            (
                {
                    'test': 'ok',
                },
            ),
            extractor.is_met(values).values()
        )

    def test_multiple_values(self):
        extractor = DictExtractFields(type=None, fields=[
            'test',
            'hi',
        ])
        values = ValuesCollection((
            {
                'hi': 'hi',
                'test': 'ok',
            },
            {
                'hi': 'hi2',
                'test': 'test2',
            },
        ))

        self.assertEqual((
            {
                'test': 'ok',
                'hi': 'hi',
            },
            {
                'hi': 'hi2',
                'test': 'test2',
            }
        ),

            extractor.is_met(values).values()
        )
