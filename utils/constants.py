from dotenv import load_dotenv
import os

# Environment Variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')
SAVE_CHANNEL = int(os.getenv('SAVE_CHANNEL'))