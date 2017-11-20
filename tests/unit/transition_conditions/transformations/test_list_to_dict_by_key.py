import unittest

from funcytaskengine.transition_conditions.transformations import ListToDictByKey


class ListToDictByKeyTestCase(unittest.TestCase):
    def test_no_values(self):
        t = ListToDictByKey(type=None, by_key='test')
        EMPTY_DICT = {}
        EMPTY_LIST = []
        self.assertEqual(EMPTY_DICT, t.is_met(EMPTY_LIST))

    def test_one_value(self):
        t = ListToDictByKey(type=None, by_key='test1')
        self.assertEqual(
            {
                'test1': {
                    'test1': 'test1',
                    'test2': 'test2',
                }
            },

            t.is_met([
                {
                    'test1': 'test1',
                    'test2': 'test2',
                }
            ])
        )

    def test_many_values(self):
        t = ListToDictByKey(type=None, by_key='test1')
        self.assertEqual(
            {
                'test1': {
                    'test1': 'test1',
                    'test2': 'test2',
                },
                'second_test': {
                    'test1': 'second_test',
                    'test2': 'test2',
                }
            },

            t.is_met([
                {
                    'test1': 'test1',
                    'test2': 'test2',
                },
                {
                    'test1': 'second_test',
                    'test2': 'test2',
                }
            ])
        )

    def test_duplicate_values(self):
        t = ListToDictByKey(type=None, by_key='test1')
        self.assertEqual(
            {
                'test1': {
                    'test1': 'test1',
                    'test2': 'test2',
                }
            },

            t.is_met([
                {
                    'test1': 'test1',
                    'test2': 'test2',
                },
                {
                    'test1': 'test1',
                    'test2': 'test2',
                }
            ])
        )
