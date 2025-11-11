'''Integrate Web socked form create list of online users'''
from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect
import json

active_connections: Dict[int, WebSocket] = {}
online_users: Dict[int,str] = {}

async def broadcast_online_users():
    '''Send list of online users all conected users'''
    online_list = [
        {"id": user_id, "username": username}
        for user_id, username in online_users.items()
    ]

    # create message
    message = {
        "type": "online_users",
        "users": online_list,
        "count": len(online_list)
    }

    # send to all

    disconnected = []
    for user_id, connection in active_connections.items():
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"Failed to send to {user_id}: {e}")
            disconnected.append(user_id)

    # Delete disconnected users
    for user_id in disconnected:
        if user_id in active_connections:
            del active_connections[user_id]
        if user_id in online_users:
            del online_users[user_id]