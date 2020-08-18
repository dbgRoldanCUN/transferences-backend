import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('/var/www/transferences') / '.env'
load_dotenv(dotenv_path=env_path)

_config = {
    'db_config':{
        'host': os.getenv("DB_HOST"),
        'port': os.getenv("DB_PORT"),
        'service': os.getenv("DB_SERVICE"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD")
    },
    'mail_config': {
        'server': os.getenv("MAIL_SERVER"),
        'port': os.getenv("MAIL_PORT"),
        'username': os.getenv("MAIL_USERNAME"),
        'password': os.getenv("MAIL_PASSWORD"),
        'mail_use_tsl': os.getenv("MAIL_USE_TSL"),
        'mail_use_ssl': os.getenv("MAIL_USE_SSL"),
        'template': os.getenv("MAIL_TEMPLATE"),
    },
    'port_http': os.getenv("PORT_HTTP"),
    'host': os.getenv("HOST"),
    'mail_messages': os.getenv("MAIL_MESSAGES"),
    'upload_user_files': os.getenv("UPLOAD_FOLDER_USER")
}

def getConfig():
    return _config

