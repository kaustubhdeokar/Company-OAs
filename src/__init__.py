import configparser
from storage.db import DBStorageStrategy

# Read configuration
config = configparser.ConfigParser()
config.read('config.properties')
storage_type = config.get('DEFAULT', 'storage_type')

# Initialize database if storage type is 'db'
if storage_type == 'db':
    db_storage = DBStorageStrategy()
    db_storage.init_db()