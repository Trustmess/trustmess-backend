from typing import Dict, List
from fastapi import WebSocket
import json
import datetime


class ConnectionManager:
    '''Manages WebSocket connections and online users'''

    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.online_users: Dict[int, str] = {}
        self.chat_messages: Dict[str, List[dict]] = {}
    
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

    async def send_personal_message(self, message: dict, user_id: int):
        '''Send message to user'''
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
            except Exception as error:
                print(f'Error sending message to user {user_id}: {error}')

    async def handle_message(self, data: dict, sender_id: int ):
        '''Handle input message'''
        message_type = data.get('type')

        if message_type == 'chat_message':
            # Message in chat
            recipient_id = data.get('recipient_id')
            content = data.get('content')
            timestamp = data.get('timestamp', datetime.utcnow().isoformat())

            # Create message for sending 
            message = {
                "type": "chat_message",
                "sender_id": sender_id,
                "recipient_id": recipient_id,
                "content": content,
                "timestamp": timestamp,
                "message_id": data.get("message_id")  # ? It's in example, for what this? 
            }

            # Send to recip user
            await self.send_personal_message(message, recipient_id)

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