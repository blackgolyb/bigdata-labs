import asyncio

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import *

from app.api import router as control_router
from app.consumer_app import ConsumerApp
from app.models import Orders
from services.websocket_manager import ConnectionManager


logger = logging.getLogger("uvicorn")


def configure_fastapi():
    app = FastAPI(title="lab2-consumer", debug=DEBUG)

    app.include_router(control_router)

    origins = [
        f"http://{SERVER_HOST}:{SERVER_PORT}",
        f"https://{SERVER_HOST}:{SERVER_PORT}",
        f"ws://{SERVER_HOST}:{SERVER_PORT}",
        f"wss://{SERVER_HOST}:{SERVER_PORT}",
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
    app = ConsumerApp(topic=KAFKA_TOPIC, kafka_urls=f"{KAFKA_HOST}:{KAFKA_PORT}")
    ws = ConnectionManager()

    async def broadcast(orders: Orders):
        await ws.broadcast(orders.model_dump_json())

    app.on_best_orders_changes.connect(broadcast)

    if LOGGING:

        async def log_info(orders: Orders):
            for order_type in ["order_created", "order_changed", "order_deleted"]:
                table = ""
                for order in orders[order_type]:
                    table += f"price: {order.data.price}\tid: {order.data.id}\n"

                logger.info(f"{order_type}: \n{table}")

        app.on_best_orders_changes.connect(log_info)

    return app


def configure_uvicorn(fasapi_app):
    config = uvicorn.Config(
        fasapi_app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level="info",
    )

    return uvicorn.Server(config)


async def main():
    fasapi_app = configure_fastapi()
    consumer_app = configure_consumer_app()
    server = configure_uvicorn(fasapi_app)

    async with consumer_app:
        await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
