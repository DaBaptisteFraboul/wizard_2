# coding: utf-8

# Python modules
import logging

# Wizard modules
from wizard.vars import user_vars

def get_logger(name=None):
    # create logger
    logging_level = logging.INFO

    file = user_vars._user_logging_file_

    logging.basicConfig(level=logging_level,
        format="%(asctime)s [%(name)-23.23s] [%(levelname)-5.5s] %(message)s")
    
    if name:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger()

    return logger