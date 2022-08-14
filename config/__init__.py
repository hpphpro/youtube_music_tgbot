import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ROOT_DIR = Path(__file__).resolve().parent.parent

TOKEN = os.environ.get('TOKEN')
