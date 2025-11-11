from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    '''Manages WebSocket connections and online users'''

    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.online_users: Dict[int, str] = {}
    
    async def connect(self, user_id: int, username: str, websocket: WebSocket):
        '''Add new connection'''
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.online_users[user_id] = username
        print(f"User {user_id} ({username}) connected")
        await self.broadcast_online_users()

    async def disconnect(self, user_id: int):
        '''Remove connection'''

        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.online_users:
            del self.online_users[user_id]
    
    async def broadcast_online_users(self):
        '''Send list of online users to all connected users'''
        online_list = [
            {"id": user_id, "username": username}
            for user_id, username in self.online_users.items()
        ]

        message = {
            "type": "online_users",
            "users": online_list,
            "count": len(online_list)
        }

        disconnected = []
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except Exception as error:
                print(f"Failed to send to {user_id}: {error}")
                disconnected.append(user_id)
        
        # Clean up disconnected
        for user_id in disconnected:
            await self.disconnect(user_id)

    def get_online_count(self) -> int:
        '''Get count of online users'''
        return len(self.online_users)
    
    def get_online_list(self) -> list:
        '''Get list of online users'''
        return[
            {'id': user_id, "username": username}
            for user_id, username in self.online_users.items()
        ]
    

# Singleton instance
manager = ConnectionManager()