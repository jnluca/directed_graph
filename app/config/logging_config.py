import logging
import logging.config
import os
from datetime import datetime

from app.utils import create_dir_if_not_exist


def set_logging_config() -> None:
    config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] - %(levelname)s - %(name)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'directed_graph_handler': {
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': os.path.join(get_log_directory(), 'tmp', f'{today()}_directed_graph.log')
            }
        },
        'loggers': {
            'DirectedGraph': {
                'level': 'INFO',
                'handlers': ['directed_graph_handler']
            }
        }
    }
    create_dir_if_not_exist(get_log_directory())
    logging.config.dictConfig(config)


def today() -> str:
    return datetime.today().strftime('%Y%m%d')


def get_log_directory() -> str:
    return os.path.dirname(os.path.dirname(__file__))


class Logger:

    def __init__(self, logger_name: str):
        self.logger_name = logger_name

    def create(self):
        return logging.getLogger(self.logger_name)
