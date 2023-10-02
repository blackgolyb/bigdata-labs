import json

from kafka import KafkaConsumer

from config import *


def main():
    consumer = KafkaConsumer(
        "bitstamp",
        bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
    )

    for msg in consumer:
        print(msg.value)


if __name__ == "__main__":
    main()


# {
#     "data": {
#         "id": 1668902609674242,
#         "id_str": "1668902609674242",
#         "order_type": 1,
#         "datetime": "1696281903",
#         "microtimestamp": "1696281903146000",
#         "amount": 1.07512726,
#         "amount_str": "1.07512726",
#         "amount_traded": "0.00184000",
#         "amount_at_create": "1.07696726",
#         "price": 27856,
#         "price_str": "27856",
#     },
#     "channel": "live_orders_btcusd",
#     "event": "order_changed",
# }
