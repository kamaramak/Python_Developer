import os
from string import ascii_letters

from dotenv import load_dotenv

load_dotenv()
SYMBOLS = ascii_letters + "0123456789"
DISK_TOKEN = os.environ.get("DISK_TOKEN")
API_HOST = "https://cloud-api.yandex.net/"
API_VERSION = "v1"
UPLOAD_LINK = f"{API_HOST}{API_VERSION}/disk/resources/upload"
DOWNLOAD_LINK = f"{API_HOST}{API_VERSION}/disk/resources/download"
AUTH_HEADERS = {"Authorization": f"OAuth {DISK_TOKEN}"}
