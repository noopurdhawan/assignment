import os
import logging
import configparser

logging.basicConfig(filename='error.log', level=logging.INFO)

try:
    parser = configparser.ConfigParser()
    parser.read('user_config.ini')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(parser['user_settings']['filename'])
    from app import app

except Exception as e:
    logging.info(e)
