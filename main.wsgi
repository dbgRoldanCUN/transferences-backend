import sys
sys.path.insert(0, '/var/www/transferences')
from src.main import app as application

if __name__ == "__main__":
    application.run()
