import logging 
import sys

def get_logger():
    """
    A function that returns a logger
    """
    logger = logging.getLogger("soil-organic-carbon-prediction")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = get_logger()
