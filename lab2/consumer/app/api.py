from fastapi import WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

# import config
# from config import templates
# from services.utils import get_all_nodes_hosts, collect_url
# from services.websocket_manager import ws_manager
# from services import nodes_api
# from services.lamport_clock import lamport_clock
# from apps.models import Message, Mail, ControlMessage, ActiveNode, ActiveNodes


router = APIRouter()
# url_by_name = {}


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # all_nodes = get_all_nodes_hosts()

    # active_nodes = await nodes_api.get_active_nodes(all_nodes)
    # active_nodes_names = await nodes_api.get_nodes_names(active_nodes)

    # # FIXME:
    # global url_by_name
    # url_by_name = active_nodes_names


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
