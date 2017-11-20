import unittest

from funcytaskengine.transition_conditions.transformations import DictExtractFields


class DictExtractFieldsTestCase(unittest.TestCase):

    def test_no_values(self):
        extractor = DictExtractFields(type=None, fields=['test'])
        EMPTY_LIST = []
        self.assertEqual(EMPTY_LIST, extractor.is_met(EMPTY_LIST))

    def test_single_value(self):
        extractor = DictExtractFields(type=None, fields=['test'])
        values = [
            {
                'hi': 'hello',
                'test': 'ok',
            },
        ]

        self.assertEqual([
            {
                'test': 'ok',
            }
        ], extractor.is_met(values))

    def test_multiple_values(self):
        extractor = DictExtractFields(type=None, fields=[
            'test',
            'hi',
        ])
        values = [
            {
                'hi': 'hi',
                'test': 'ok',
            },
            {
                'hi': 'hi2',
                'test': 'test2',
            },
        ]

        self.assertEqual([
            {
                'test': 'ok',
                'hi': 'hi',
            },
            {
                'hi': 'hi2',
                'test': 'test2',
            }
        ], extractor.is_met(values))
