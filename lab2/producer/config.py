from envparse import Env

env = Env()

DEBUG = env.bool("DEBUG", default=True)

BITSTAMP_URL = env.str("BITSTAMP_URL", default="wss://ws.bitstamp.net/")
BITSTAMP_CHANNEL = env.str("BITSTAMP_CHANNEL", default="live_orders_btcusd")

KAFKA_TOPIC = env.str("KAFKA_TOPIC", default="bitstamp")
KAFKA_HOST = env.str("KAFKA_HOST", default="0.0.0.0")
KAFKA_PORT = env.int("KAFKA_PORT", default=29092)
