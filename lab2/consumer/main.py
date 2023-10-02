import json

from pydantic import BaseModel
from kafka import KafkaConsumer

from config import *


class OrderData(BaseModel):
    id: int
    id_str: str
    order_type: int
    datetime: str
    microtimestamp: str
    amount: float
    amount_str: str
    amount_traded: str
    amount_at_create: str
    price: int
    price_str: str


class Order(BaseModel):
    data: OrderData
    channel: str
    event: str

    def get_price(self):
        return self.data.price

    def __lt__(self, other):
        return self.data.price < other.data.price

    def __le__(self, other):
        return self.data.price <= other.data.price

    def __eq__(self, other):
        return self.data.price == other.data.price

    def __ne__(self, other):
        return self.data.price != other.data.price

    def __gt__(self, other):
        return self.data.price > other.data.price

    def __ge__(self, other):
        return self.data.price >= other.data.price


class App(object):
    def __init__(self, kafka_urls: str | list[str], topic: str):
        self.best_orders = dict()
        self.configure_kafka(kafka_urls, topic)

    def configure_kafka(self, kafka_urls: str | list[str], topic: str):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=kafka_urls,
            value_deserializer=lambda m: json.loads(m.decode("ascii")),
        )

    def process_message(self, message: dict):
        order = Order.parse_obj(message)

        if order.event not in self.best_orders:
            self.best_orders[order.event] = list()
            self.best_orders[order.event].append(order)
            return

        if order > min(self.best_orders[order.event]):
            if len(self.best_orders[order.event]) >= 10:
                self.best_orders[order.event].pop()

            self.best_orders[order.event].append(order)

        self.best_orders[order.event].sort(reverse=True)

    def start(self):
        for message in self.consumer:
            self.process_message(message.value)


def main():
    app = App(topic=KAFKA_TOPIC, kafka_urls=f"{KAFKA_HOST}:{KAFKA_PORT}")
    app.start()


if __name__ == "__main__":
    main()
