from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.db import queries
from src.websocket.managed import manager
import json

router = APIRouter()


# ? websocket /ws/{user_id}
# *****************************************************************************
@router.websocket("/ws/{user_id}", name="NONE")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    WebSocket connection for control online status
    """

    # Get user info from DB
    user = queries.get_user_by_id(user_id)

    if not user:
        await websocket.close(code=1008, reason="User not found")
        return

    # Connect user
    await manager.connect(user_id, user["username"], websocket)

    try:
        # Keep connection alive
        while True:
            data = await websocket.receive_text()

            message_data = json.loads(data)
            await manager.handle_message(message_data, user_id)

            print(f"Received from {user_id}: {data}")

    except WebSocketDisconnect:
        await manager.disconnect(user_id)
        await manager.broadcast_online_users()
    except Exception as error:
        print(f"WebSocket error for user {user_id}: {error}")
        await manager.disconnect(user_id)
        await manager.broadcast_online_users()


# *****************************************************************************


# * GET
# *****************************************************************************
@router.get("/ws/online", name="list_online_users", tags=["Websockets"])
async def get_online_user():
    """Get list of currently online users"""
    return {
        "status": "success",
        "users": manager.get_online_list(),
        "count": manager.get_online_count(),
    }


# *****************************************************************************
