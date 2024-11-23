import json
from datetime import datetime
from app.application.redis import redis_manager


class RedisHardwareConnectionManager:
    def __init__(self):
        self.session = redis_manager.get_connection()
        self.user_sessions_key = "user_hardware_sessions"

    async def connect(
        self,
        hardware_id: str,
        user_id: str,
        hardware_type: str,
    ) -> None:
        if not await self.session.hexists(self.user_sessions_key, user_id):
            await self.session.hset(
                self.user_sessions_key,
                user_id,
                json.dumps(
                    {
                        "display": {},
                        "camera": {},
                        "created_at": datetime.now().isoformat(),
                    }
                ),
            )
        data = json.loads(await self.session.hget(self.user_sessions_key, user_id))
        if hardware_type == "display":
            data["display"] = {"hardware_id": hardware_id}
            await self.session.hset(self.user_sessions_key, user_id, json.dumps(data))
        elif hardware_type == "camera":
            data["camera"] = {"hardware_id": hardware_id}
            await self.session.hset(self.user_sessions_key, user_id, json.dumps(data))

    async def disconnect(self, user_id: str, hardware_type: str) -> None:
        if await self.session.hexists(self.user_sessions_key, user_id):
            data = json.loads(await self.session.hget(self.user_sessions_key, user_id))
            if hardware_type == "display":
                data["display"] = {}
            elif hardware_type == "camera":
                data["camera"] = {}
            await self.session.hset(self.user_sessions_key, user_id, json.dumps(data))
