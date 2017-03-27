from funcytestengine.engine import TaskEngine
from funcytestengine.machine import TaskMachine, STATES

import yaml
from nose import run
from nose.loader import TestLoader

from parameterized import parameterized


def test_main(file_name):
    with open(file_name) as f:
        state_dict = yaml.load(f)

    machine = TaskMachine(machine_dict=state_dict)
    assert machine.state == STATES.PENDING
    engine = TaskEngine(machine)
    result = engine.run()
    assert result == True
    print(state_dict)


class UnittestTaskExecutor(object):
    def __init__(self, arguments):
        self.config = arguments.config
        self.single_test = arguments.single_test

    def tests_to_run(self):
        if self.single_test:
            return [self.single_test]

        raise NotImplementedError()

    def run(self):
        p = parameterized(self.tests_to_run())
        test = p(test_main)

        suite = TestLoader().loadTestsFromGenerator(
            test, __name__)

        run(argv=['-s'], suite=suite)
