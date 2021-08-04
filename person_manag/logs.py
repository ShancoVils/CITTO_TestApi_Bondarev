import logging
from logging.handlers import RotatingFileHandler
import os 


logger = logging.getLogger('person_logger')

logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# options

file_heandler = logging.FileHandler('logs/logs.log')
file_heandler.setLevel(logging.DEBUG)

file_heandler.setFormatter(formatter)

logger.addHandler(file_heandler)
    