import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
TOKEN_API = os.getenv('BOT_TOKEN')
ADMIN_ID_1 = os.getenv('ADMIN_ID_1')
ADMIN_ID_2 = os.getenv('ADMIN_ID_2')