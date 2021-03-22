import os
import logging
import configparser

# create the logging file  for status
logging.basicConfig(filename='status_log_file.log', level=logging.INFO)

try:
    """Read the user_configurations and set the key.json file 
     required for the Google Cloud Platform for BigQuery
    """
    parser = configparser.ConfigParser()
    parser.read('user_config.ini')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(parser['user_settings']['filename'])
    if os.environ["GOOGLE_APPLICATION_CREDENTIALS"]:
        logging.info('Configurations done with file:{} '.format(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')))
        # run flask app services
        from app import app
    else:
        logging.info('Please check the config file settings.')
        # abort services if config file is empty
        os.abort()

except Exception as e:
    logging.info(e)
