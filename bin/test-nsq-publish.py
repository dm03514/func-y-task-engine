import argparse
import copy
import json

import gnsq


def main(args):
    print(args)

    message = {
        'from': 'test-nsq-publish.py',
        'message': 'hi-{}',
    }

    for i in range(args.num_messages):
        m = copy.copy(message)
        m['number'] = i
        m['message'] = m['message'].format(i)
        print('Sending message: {}'.format(m))
        gnsq.Nsqd(address=args.nsqd_address).publish(
            args.topic,
            json.dumps(m)
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NSQ Fake Message Publisher')
    parser.add_argument('-t', '--topic', type=str)
    parser.add_argument('-n', '--num-messages', type=int)
    parser.add_argument('--nsqd-address', default='localhost')
    args = parser.parse_args()

    main(args)
