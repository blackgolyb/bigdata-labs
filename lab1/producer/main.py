import asyncio
import json

# from websockets.sync.client import connect
from websockets.client import connect
import time

from config import *


class SubscribeFailed(ValueError):
    ...


class TaskAlreadyStopped(ValueError):
    ...


class App(object):
    BITSTAMP_URL = BITSTAMP_URL

    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.tasks = []

    def get_subscribe_request_data(self, channel):
        return json.dumps(
            {
                "event": "bts:subscribe",
                "data": {"channel": channel},
            }
        )

    def check_is_subscribe_correct(self, channel, subscribe_message):
        message_data = json.loads(subscribe_message)
        event = message_data.get("event", None)
        channel_from_message = message_data.get("channel", None)

        if event == "bts:subscription_succeeded" and channel_from_message == channel:
            return
        raise SubscribeFailed(f"cannot subscribe to chanel {channel}")

    async def run_customer_receiver(self, websocket, callback):
        while True:
            raw_message = await websocket.recv()
            message = json.loads(raw_message)
            # print("lol")
            # print(f"Message: {message}")
            await callback(message)

    async def run(self, channel, message_receiver_callback):
        subscribe_request_data = self.get_subscribe_request_data(channel)

        async with connect(self.BITSTAMP_URL) as websocket:
            await websocket.send(subscribe_request_data)

            subscribe_received_message = await websocket.recv()
            self.check_is_subscribe_correct(channel, subscribe_received_message)

            await self.run_customer_receiver(websocket, message_receiver_callback)

    def create_task(self, channel, message_receiver):
        task = self.loop.create_task(self.run(channel, message_receiver))
        self.tasks.append(task)
        return task

    def stop_task(self, task):
        if task not in self.tasks:
            raise TaskAlreadyStopped("Task: {task} has already been stopped")

        self.tasks.remove(task)
        task.cancel()

    def stop_all(self):
        for task in self.tasks:
            task.cancel()


async def process_message(message):
    # await asyncio.sleep(0.001)
    print(f"Message: {message}")


async def main():
    app = App()

    task = app.create_task(channel=BITSTAMP_CHANNEL, message_receiver=process_message)
    await asyncio.sleep(5)
    app.stop_task(task)


if __name__ == "__main__":
    asyncio.run(main())


# {
#     "data": {
#         "id": 1668878635663360,
#         "id_str": "1668878635663360",
#         "order_type": 0,
#         "datetime": "1696276048",
#         "microtimestamp": "1696276047931000",
#         "amount": 0.00179676,
#         "amount_str": "0.00179676",
#         "amount_traded": "0",
#         "amount_at_create": "0.00179676",
#         "price": 27825,
#         "price_str": "27825",
#     },
#     "channel": "live_orders_btcusd",
#     "event": "order_deleted",
# }
