import unittest

from funcytaskengine.event_fulfillment.return_values import ValuesWrappedContainer, ValuesCollection, EmptyValues
from funcytaskengine.transition_conditions.transformations import ListToDictByKey


class ListToDictByKeyTestCase(unittest.TestCase):
    def test_no_values(self):
        t = ListToDictByKey(type=None, by_key='test')
        self.assertEqual(
            ValuesWrappedContainer({}).values(),
            t.is_met(EmptyValues()).values(),
        )

    def test_one_value(self):
        t = ListToDictByKey(type=None, by_key='test1')
        self.assertEqual(
            (
                {
                    'test1': {
                        'test1': 'test1',
                        'test2': 'test2',
                    }
                },
            ),

            t.is_met(
                ValuesWrappedContainer(
                    {
                        'test1': 'test1',
                        'test2': 'test2',
                    }
                )
            ).values()
        )

    def test_many_values(self):
        t = ListToDictByKey(type=None, by_key='test1')
        self.assertEqual((
            {
                'test1': {
                    'test1': 'test1',
                    'test2': 'test2',
                },
                'second_test': {
                    'test1': 'second_test',
                    'test2': 'test2',
                }
            },),

            t.is_met(
                ValuesCollection([
                    {
                        'test1': 'test1',
                        'test2': 'test2',
                    },
                    {
                        'test1': 'second_test',
                        'test2': 'test2',
                    }
                ])
            ).values()
        )

    def test_duplicate_values(self):
        t = ListToDictByKey(type=None, by_key='test1')
        self.assertEqual(
            (
                {
                    'test1': {
                        'test1': 'test1',
                        'test2': 'test2',
                    }
                },
            ),

            t.is_met(
                ValuesCollection(
                    [
                        {
                            'test1': 'test1',
                            'test2': 'test2',
                        },
                        {
                            'test1': 'test1',
                            'test2': 'test2',
                        }
                    ]
                )
            ).values()
        )
