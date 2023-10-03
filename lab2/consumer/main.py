import json
import asyncio
from enum import Enum, EnumMeta

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from aiokafka import AIOKafkaConsumer

from config import *
from app.api import router as control_router
from services.signal import AsyncSignal
from services.websocket_manager import ConnectionManager


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class OrdersEvents(str, Enum, metaclass=MetaEnum):
    ORDER_CREATED = "order_created"
    ORDER_CHANGED = "order_changed"
    ORDER_DELETED = "order_deleted"


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


class Orders(BaseModel):
    order_created: list[Order] = list()
    order_changed: list[Order] = list()
    order_deleted: list[Order] = list()

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except:
            super().__getitem__(key)

    def __contains__(self, key):
        try:
            return hasattr(self, key)
        except:
            super().__getitem__(key)

    def __setitem__(self, key, value):
        try:
            setattr(self, key, value)
        except:
            super().__getitem__(key)


class App(object):
    def __init__(self, kafka_urls: str | list[str], topic: str, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.task = None
        self.best_orders = Orders()
        self.on_best_orders_changes = AsyncSignal()
        self.configure_kafka(kafka_urls, topic)

    def configure_kafka(self, kafka_urls: str | list[str], topic: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=kafka_urls,
            value_deserializer=lambda m: json.loads(m.decode("ascii")),
        )

    async def process_message(self, message: dict):
        event = message.get("event", None)
        if event not in OrdersEvents:
            return

        order = Order.parse_obj(message)

        if not self.best_orders[order.event]:
            self.best_orders[order.event].append(order)
            await self.on_best_orders_changes.emit(self.best_orders)

        elif order > min(self.best_orders[order.event]):
            if len(self.best_orders[order.event]) >= 10:
                self.best_orders[order.event].pop()

            self.best_orders[order.event].append(order)
            self.best_orders[order.event].sort(reverse=True)

            await self.on_best_orders_changes.emit(self.best_orders)

    async def run(self):
        await self.consumer.start()
        try:
            async for message in self.consumer:
                await self.process_message(message.value)
        finally:
            await self.consumer.stop()

    async def start(self):
        if self.task:
            self.stop()

        self.task = self.loop.create_task(self.run())

    async def stop(self):
        self.task.cancel()

    async def __aenter__(self):
        await self.start()

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        await self.stop()


def configure_fastapi():
    # create instance of the app
    app = FastAPI(title="lab2-consumer", debug=DEBUG)

    app.include_router(control_router)

    origins = [
        f"http://{SERVER_HOST}:{SERVER_PORT}",
        f"ws://{SERVER_HOST}:{SERVER_PORT}",
    ]

    app = CORSMiddleware(
        app=app,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def configure_consumer_app():
    app = App(topic=KAFKA_TOPIC, kafka_urls=f"{KAFKA_HOST}:{KAFKA_PORT}")
    ws = ConnectionManager()

    async def broadcast(orders: Orders):
        await ws.broadcast(orders.model_dump_json())

    app.on_best_orders_changes.connect(broadcast)

    return app


async def main():
    fasapi_app = configure_fastapi()
    consumer_app = configure_consumer_app()

    config = uvicorn.Config(
        fasapi_app, host=SERVER_HOST, port=SERVER_PORT, log_level="info"
    )
    server = uvicorn.Server(config)

    async with consumer_app:
        await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
