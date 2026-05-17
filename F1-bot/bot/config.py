import os

from dotenv import load_dotenv

load_dotenv(override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
TEST_BOT_TOKEN = os.getenv("TEST_BOT_TOKEN")
LOCAL_TEST_BOT_TOKEN = os.getenv("LOCAL_TEST_BOT_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")
TEST_REDIS_URL = os.getenv("TEST_REDIS_URL")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
TESTER_ID = int(os.getenv("TESTER_ID", "0"))
MAIN_BOT_LINK = os.getenv("MAIN_BOT_LINK")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
