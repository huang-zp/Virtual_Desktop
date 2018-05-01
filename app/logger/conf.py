import os
APP_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] - [%(levelname)-8s] - [%(name)-8s] - [%(message)s]',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '[%(blue)s%(asctime)s%(reset)s] - [%(log_color)s%(levelname)-8s%(reset)s] - '
                      '[%(purple)s%(name)-8s%(reset)s] - [%(cyan)s%(message)s%(reset)s]',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG': 'white',
                'INFO': 'bold_green',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'red,bg_white'
            }
        }
    },
    'handlers': {
        'task': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/task/task.log'.format(APP_PATH),
            'formatter': 'standard'
        },
        'console': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'colored'
        },
        'api': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/api/api.log'.format(APP_PATH),
            'formatter': 'standard'
        },
        'freebuf': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/freebuf/freebuf.log'.format(APP_PATH),
            'formatter': 'standard'
        },
        'cnnvd': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/cnnvd/cnnvd.log'.format(APP_PATH),
            'formatter': 'standard'
        },
        'hackernews': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/hackernews/hackernews.log'.format(APP_PATH),
            'formatter': 'standard'
        },
        'cnvd': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/cnvd/cnvd.log'.format(APP_PATH),
            'formatter': 'standard'
        },
        'crawl': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/crawl/crawl.log'.format(APP_PATH),
            'formatter': 'standard'
        },
        'sync_sqlite': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/sync_sqlite/sync_sqlite.log'.format(APP_PATH),
            'formatter': 'standard'
        },
        'threat_domain': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/threat_domain/threat_domain.log'.format(APP_PATH),
            'formatter': 'standard'
        },
        'threat_ip': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/threat_ip/threat_ip.log'.format(APP_PATH),
            'formatter': 'standard'
        }
,
        'show': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'filename': '{}/logs/show/show.log'.format(APP_PATH),
            'formatter': 'standard'
        }
    },
    'loggers': {
        'task': {
            'handlers': ['task', 'console'],
            'propagate': False
        },
        'api': {
            'handlers': ['api', 'console'],
            'propagate': False
        },
        'task_freebuf': {
            'handlers': ['freebuf', 'console'],
            'propagate': False
        },
        'task_cnnvd': {
            'handlers': ['cnnvd', 'console'],
            'propagate': False
        },
        'task_cnvd': {
            'handlers': ['cnvd', 'console'],
            'propagate': False
        },
        'task_hackernews': {
            'handlers': ['hackernews', 'console'],
            'propagate': False
        },
        'crawl': {
            'handlers': ['crawl', 'console'],
            'propagate': False
        },
        'sync_sqlite': {
            'handlers': ['sync_sqlite', 'console'],
            'propagate': False
        },
        'threat_domain': {
            'handlers': ['threat_domain', 'console'],
            'propagate': False
        },
        'threat_ip': {
            'handlers': ['threat_ip', 'console'],
            'propagate': False
        }
,
        'show': {
            'handlers': ['show', 'console'],
            'propagate': False
        }

    }
}
