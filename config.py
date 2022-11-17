import configparser
import os
from pathlib import Path


path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

try:
    SERVER_API_URL_UPLOAD = config.get('SERVER_API', 'URL_UPLOAD_RESULT')
    SERVER_API_TOKEN = config.get('SERVER_API', 'TOKEN')
except configparser.ConfigParser.NoOptionError:
    print('could not read configuration file')