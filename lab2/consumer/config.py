from fastapi.templating import Jinja2Templates
from envparse import Env

env = Env()

DEBUG = env.bool("DEBUG", default=True)

KAFKA_HOST = env.str("KAFKA_HOST", default="0.0.0.0")
KAFKA_PORT = env.int("KAFKA_PORT", default=29092)
KAFKA_TOPIC = env.str("KAFKA_TOPIC", default="bitstamp")

SERVER_HOST = env.str("SERVER_HOST", default="0.0.0.0")
SERVER_PORT = env.int("SERVER_PORT", default=8080)


templates = Jinja2Templates(directory="templates")
