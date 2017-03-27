import yaml
from nose import run
from nose.loader import TestLoader

from parameterized import parameterized

import funcytestengine
from funcytestengine.unittesttaskexecutor import test_main



if __name__ == '__main__':
    p = parameterized([
        ('tests/fixtures/simple_http_test.yml',),
        ('tests/fixtures/multi_state_test.yml',),
    ])
    test = p(test_main)

    suite = TestLoader().loadTestsFromGenerator(
        test, funcytestengine.unittesttaskexecutor)

    run(argv=['-s'], suite=suite)
