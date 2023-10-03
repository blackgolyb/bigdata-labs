import asyncio
import json

from aiokafka import AIOKafkaConsumer

from app.models import Orders, OrdersEvents, Order
from services.signal import AsyncSignal


class ConsumerApp(object):
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
