import configparser


CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

SERVER_API_URL_UPLOAD = config.get('SERVER_API', 'URL_UPLOAD_RESULT')
SERVER_API_TOKEN = config.get('SERVER_API', 'TOKEN')
