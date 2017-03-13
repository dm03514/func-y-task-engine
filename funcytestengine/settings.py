import logging

import sys

from os import getenv

ENGINE_LOOP_INTERVAL = float(getenv('ENGINE_LOOP_INTERVAL', 0.020))


root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)