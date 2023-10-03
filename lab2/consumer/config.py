from fastapi.templating import Jinja2Templates


KAFKA_HOST = "0.0.0.0"
KAFKA_PORT = 29092
KAFKA_TOPIC = "bitstamp"

DEBUG = True
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080


templates = Jinja2Templates(directory="templates")
