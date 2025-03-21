import os

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

COMMON_PREFIX = "/api/v1"
CACHE_TIME_SEC = 60 * 10
