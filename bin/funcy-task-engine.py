import argparse

from funcytestengine.unittesttaskexecutor import UnittestTaskExecutor


def run(arguments):
    ute = UnittestTaskExecutor(arguments)
    ute.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Func-y Task Engine!')
    subparsers = parser.add_subparsers(help='subparser help')

    run_parser = subparsers.add_parser('run', help='run help')
    run_parser.add_argument(
        '-c', '--config', type=str, default='.func-y-test.yml', dest='config')
    run_parser.add_argument(
        '-t', '--test', type=str, default=None, dest='single_test')
    run_parser.set_defaults(func=run)

    args = parser.parse_args()
    args.func(args)

