# ? WebSocket endpoints
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    WebSocket connection for control online status
    """
    # Get connection
    await websocket.accept()
    print(f"User {user_id} connecnted")

    # Get info user info from DB
    conn = db_connector.get_db_connection(db_connector.DB_PATH_MAIN)
    user = db_connector.get_user_by_id(conn, user_id)
    conn.close()

    if not user:
        await websocket.close()
        return
    
    # Add active connection
    active_connections[user_id] = websocket
    online_users[user_id] = user['username']

    await broadcast_online_users()

    try:
        # wain new messege (support connection)
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        # User disconnect
        print(f"User {user_id} disconnected")

        # Delete user from active users
        if user_id in active_connections:
            del active_connections[user_id]
        if user_id in online_users:
            del online_users[user_id]

        # "Say" all about update
        await broadcast_online_users()


# ! DEV ROUTE
@app.get("/dev/online_debug", name="Debug Online Users", tags=["dev"])
async def debug_online_users():
    """DEV: info about online users"""
    return {
        "status": "debug",
        "online_users": dict(online_users),  # {id: username}
        "active_connections_count": len(active_connections),
        "connection_ids": list(active_connections.keys()),
        "full_list": [
            {"id": user_id, "username": username}
            for user_id, username in online_users.items()
        ]
    }