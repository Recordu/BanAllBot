import dotenv
from os import getenv

dotenv.load_dotenv('local.env')

API_ID = getenv('API_ID')
API_HASH = getenv('API_HASH')
BOT_TOKEN = getenv('BOT_TOKEN')
USERS = {int(x) for x in getenv("SUDO_USERS", "").split()}
DB_URL = getenv('DATABASE_URL')  