import glob

import os

from funcytaskengine.engine import TaskEngine
from funcytaskengine.machine import TaskMachine, STATES

import yaml
import xmlrunner
from nose.loader import TestLoader
from gevent import monkey

from parameterized import parameterized

from funcytaskengine.templateprocessors.environmentalvariable import EnvironmentalVariableTemplateProcessor
from funcytaskengine.templateprocessors.unique import UUIDStringTemplateProcessor

TEMPLATE_PROCESSORS = [
    EnvironmentalVariableTemplateProcessor(),
    UUIDStringTemplateProcessor(),
]


def test_individual(file_name):
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
    print(state_dict)

    machine = TaskMachine(machine_dict=state_dict)
    assert machine.state == STATES.PENDING
    engine = TaskEngine(machine)
    result = engine.run()
    assert result


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


class TaskExecutor(object):

    def __init__(self, arguments):
        self.config_loader = ConfigTestLoader(
            arguments.root_dir,
            arguments.config
        )
        self.single_test = arguments.single_test

        monkey.patch_all()

    def tests_to_run(self):
        if self.single_test:
            return [self.single_test]

        return self.config_loader.tests()

    def clean_names(self, tests):
        return tests

    def xmltest(self):
        """
        Runs each specified tests by using python unittest to execute
        and reports results through stdout and junit xml format.

        :return:
        """
        p = parameterized(
            self.clean_names(
                self.tests_to_run()
            )
        )
        test_main = p(test_individual)
        suite = TestLoader().loadTestsFromGenerator(test_main, __name__)
        testRunner = xmlrunner.XMLTestRunner(output='test-reports')
        testRunner.run(suite)

    def run(self):
        """
        Runs the specified test files by calling them directly.

        :return:
        """
        for test_file in self.tests_to_run():
            test_individual(test_file)
