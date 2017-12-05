import logging.config
import sys

DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_LOG_LEVEL = 'DEBUG'

'''
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter()
ch.setFormatter(formatter)
root.addHandler(ch)
'''

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': DEFAULT_LOG_FORMAT,
        },
        'json': {
            'format': DEFAULT_LOG_FORMAT,
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': DEFAULT_LOG_LEVEL,
    },
}

logging.config.dictConfig(LOGGING)
