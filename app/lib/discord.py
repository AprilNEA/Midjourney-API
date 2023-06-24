from typing import Dict, Any

from aiohttp import ClientSession
from config import Config

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": Config.Discord.user_token,
}


def _trigger_payload(type_: int, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    payload = {
        "type": type_,
        "application_id": "936929561302675456",
        "guild_id": Config.Discord.guild_id,
        "channel_id": Config.Discord.channel_id,
        "session_id": "cb06f61453064c0983f2adae2a88c223",
        "data": data,
    }
    payload.update(kwargs)
    return payload


class MidjourneyBot:
    def __init__(self, session: ClientSession):
        self.session = session

    async def _trigger(self, payload: Dict[str, Any]):
        async with self.session.post(
            url=Config.ApiUrl.interactions, headers=HEADERS, json=payload
        ) as resp:
            if not resp.ok:
                return None
            return True

    async def generate(self, prompt: str):
        payload = _trigger_payload(
            2,
            {
                "version": "1118961510123847772",
                "id": "938956540159881230",
                "name": "imagine",
                "type": 1,
                "options": [{"type": 3, "name": "prompt", "value": prompt}],
                "attachments": [],
            },
        )
        return await self._trigger(payload)
