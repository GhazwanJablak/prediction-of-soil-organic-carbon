import logging 
import sys

def get_logger():
    logger = logging.getLogger("soil-organic-carbon-prediction")
    logger.setLevel(logging.INFO)
    formatter = "%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s"
    handler = logging.addHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = get_logger()
