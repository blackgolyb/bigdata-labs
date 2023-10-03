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

    # context = {
    #     "request": request,
    #     "all_nodes": all_nodes,
    #     "connection_update_time": config.connection_update_time,
    #     "sever_name": config.name,
    #     "sever_url": collect_url(config.server_host, config.server_port),
    # }

    return HTMLResponse("Ok")


# @router.get("/get_active_nodes/")
# async def get_active_nodes_view():
#     checked_nodes = get_all_nodes_hosts()
#     nodes = await nodes_api.get_active_nodes(checked_nodes)
#     url_by_name = await nodes_api.get_nodes_names(nodes)

#     active_nodes = []
#     for name, url in url_by_name.items():
#         active_nodes.append(
#             ActiveNode(
#                 name=name,
#                 url=url,
#             )
#         )

#     return ActiveNodes(active_nodes=active_nodes)


# @router.post("/send_mail/")
# async def send_mail(message: Message):
#     nodes = []
#     for node_name in message.receivers:
#         try:
#             nodes.append(url_by_name[node_name])
#         except:
#             ...

#     lamport_clock.update(lamport_clock.get() + len(nodes) - 1)

#     mail = Mail(
#         text=message.text,
#         sender_name=str(config.name),
#         author_name=str(config.name),
#     )

#     mail_to_control = ControlMessage(
#         type="your",
#         sender_name=mail.sender_name,
#         text=mail.text,
#         time=mail.time,
#     )
#     await ws_manager.broadcast(mail_to_control.json())

#     await nodes_api.send_mail_to_receivers(nodes, mail)


# @router.post("/send_cycle_mail/")
# async def send_mail(message: Message):
#     nodes = []
#     for node_name in message.receivers:
#         try:
#             nodes.append(url_by_name[node_name])
#         except:
#             ...

#     lamport_clock.update(lamport_clock.get() + len(nodes) - 1)
#     print("lamport_clock", lamport_clock.get(), len(nodes) - 1)

#     mail = Mail(
#         text=message.text,
#         sender_name=str(config.name),
#         author_name=str(config.name),
#         is_cycle=True,
#     )

#     mail_to_control = ControlMessage(
#         type="your",
#         sender_name=mail.sender_name,
#         text=mail.text,
#         time=mail.time,
#     )
#     await ws_manager.broadcast(mail_to_control.json())

#     await nodes_api.send_mail_to_receivers(nodes, mail)


# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await ws_manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#     except WebSocketDisconnect:
#         ws_manager.disconnect(websocket)


# @router.get("/get_clock/")
# async def get_clocks_info():
#     all_nodes = get_all_nodes_hosts()
#     active_nodes = await nodes_api.get_active_nodes(all_nodes)

#     clock_info = await nodes_api.get_clocks_info(active_nodes)

#     return {"clocks_info": clock_info}
