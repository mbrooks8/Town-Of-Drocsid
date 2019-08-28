import logging
import logging.handlers


def setup_custom_logging(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('stdout.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger

