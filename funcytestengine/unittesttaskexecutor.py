import glob
import unittest

import os

from funcytestengine.engine import TaskEngine
from funcytestengine.machine import TaskMachine, STATES

import yaml
from nose import run
from nose.loader import TestLoader

from parameterized import parameterized

from funcytestengine.templateprocessors.unique import UUIDStringTemplateProcessor

TEMPLATE_PROCESSORS = [
    UUIDStringTemplateProcessor()
]


class Test(unittest.TestCase):
    pass


def test_main(file_name):
    """
    Executes the task as a python unittest.

    Applies all template preprocessors,
    then parses the template
    executes the template
    reports the result of the task.

    :param file_name:
    :return:
    """
    with open(file_name) as f:
        task_template = f.read()

    for processor in TEMPLATE_PROCESSORS:
        task_template = processor.substitute(task_template)

    state_dict = yaml.load(task_template)

    machine = TaskMachine(machine_dict=state_dict)
    assert machine.state == STATES.PENDING
    engine = TaskEngine(machine)
    result = engine.run()
    assert result == True
    print(state_dict)


class ConfigTestLoader(object):
    def __init__(self, root_dir, config_file):
        self.root_dir = root_dir
        self.config_file = config_file

    def file_path(self):
        return os.path.join(self.root_dir, self.config_file)

    def tests(self):
        with open(self.file_path()) as f:
            config_dict = yaml.load(f)

        tests_to_execute = []
        for test in config_dict['tests']:
            globbed = glob.glob(test)
            if globbed:
                tests_to_execute.extend(globbed)
            else:
                tests_to_execute.append(test)
        return tests_to_execute


class UnittestTaskExecutor(object):

    def __init__(self, arguments):
        self.config_loader = ConfigTestLoader(arguments.root_dir, arguments.config)
        self.single_test = arguments.single_test

    def tests_to_run(self):
        if self.single_test:
            return [self.single_test]

        return self.config_loader.tests()

    def clean_names(self, tests):
        return tests
        return [t.replace('/', '').replace('.', '') for t in tests]

    def run(self):
        p = parameterized(self.clean_names(self.tests_to_run()))
        test = p(test_main)

        suite = TestLoader().loadTestsFromGenerator(
            test, __name__)

        run(argv=['', '-s', '-v', '2', '--with-xunit'], suite=suite)
