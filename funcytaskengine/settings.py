import logging.config
import sys

DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_LOG_LEVEL = 'DEBUG'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': DEFAULT_LOG_FORMAT,
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
