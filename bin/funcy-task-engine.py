import argparse

from funcytaskengine.unittesttaskexecutor import TaskExecutor


def xmltest(arguments):
    te = TaskExecutor(arguments)
    te.xmltest()


def run(arguments):
    te = TaskExecutor(arguments)
    te.run()


def xmltest_parser(subparsers):
    run_parser = subparsers.add_parser('xmltest', help='xmltest help')
    run_parser.add_argument(
        '-c', '--config', type=str, default='.func-y-test.yml', dest='config')
    run_parser.add_argument(
        '-t', '--test', type=str, default=None, dest='single_test')
    run_parser.add_argument(
        '-rt', '--root-dir', type=str, default='', dest='root_dir')
    run_parser.set_defaults(func=xmltest)


def run_parser(subparsers):
    run_parser = subparsers.add_parser(
        'run', help='runs the test by calling the functions directly, '
                    'can be used to drop into a debugger')
    run_parser.add_argument(
        '-c', '--config', type=str, default='.func-y-test.yml', dest='config')
    run_parser.add_argument(
        '-t', '--test', type=str, default=None, dest='single_test')
    run_parser.add_argument(
        '-rt', '--root-dir', type=str, default='', dest='root_dir')
    run_parser.set_defaults(func=run)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Func-y Task Engine!')

    subparsers = parser.add_subparsers(help='subparser help')

    xmltest_parser(subparsers)
    run_parser(subparsers)

    args = parser.parse_args()
    args.func(args)

