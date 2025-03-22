import os

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
TESTING = os.getenv("APP_TESTING", "False").lower() == "true"

COMMON_PREFIX = "/api/v1"
CACHE_TIME_SEC = 60 * 10
