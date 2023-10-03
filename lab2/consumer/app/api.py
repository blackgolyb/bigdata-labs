from enum import Enum

from fastapi import WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from config import *
from services.websocket_manager import ConnectionManager

router = APIRouter()
ws_manager = ConnectionManager()


class OrdersEvents(Enum):
    ORDER_CREATED = "order_created"
    ORDER_CHANGED = "order_changed"
    ORDER_DELETED = "order_deleted"


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    context = {
        "request": request,
        "HOST": SERVER_HOST,
        "PORT": SERVER_PORT,
    }
    return templates.TemplateResponse("index.html", context=context)


@router.get("/get_categories")
async def read_item(request: Request):
    return {
        "categories": list(map(lambda x: x.value, OrdersEvents._member_map_.values()))
    }


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
