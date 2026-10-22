import logging

LOG_CONFIG = {
    'version': 1,
    'formatters': {'normal': {'format': '%(levelname)-8s %(message)s'}},
    'handlers': {'console': {'class': 'logging.StreamHandler',
                             'formatter': 'normal',
                             'level': logging.INFO}},
    'loggers': {'': {'handlers': ['console'], 'level': logging.INFO}},
}
