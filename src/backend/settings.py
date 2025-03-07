import os

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

COMMON_PREFIX = "/api/v1"
