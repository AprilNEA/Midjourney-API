from typing import Dict, Any
from aiohttp import ClientSession
from config import Config


class Discord:
    def __init__(self, session: ClientSession, user_token: str = None):
        self.session = session
        self.user_token = Config.Discord.user_token if not user_token else user_token

    async def getme(self) -> Dict[str, Any]:
        async with self.session.get(
            url="https://discord.com/api/v10/users/@me",
            headers={
                "Authorization": self.user_token,
            },
        ) as resp:
            return await resp.json()

    async def join_guild(self, guild_id: str):
        user_id = (await self.getme()).get("id")
        async with self.session.put(
            url=f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}",
            headers={
                "Authorization": Config.Discord.bot_token,
            },
            json={"access_token": self.user_token},
        ) as resp:
            print(await resp.json())
            return await resp.json()


class MidjourneyBot:
    def __init__(self, session: ClientSession, setting: Dict = None):
        self.session = session
        self.setting = (
            setting
            if setting
            else {
                "user_token": Config.Discord.user_token,
                "guild_id": Config.Discord.guild_id,
                "channel_id": Config.Discord.channel_id,
            }
        )

    def _trigger_payload(
        self, type_: int, data: Dict[str, Any], **kwargs
    ) -> Dict[str, Any]:
        payload = {
            "type": type_,
            "application_id": "936929561302675456",
            "guild_id": self.setting["guild_id"],
            "channel_id": self.setting["channel_id"],
            "session_id": "cb06f61453064c0983f2adae2a88c223",
            "data": data,
        }
        payload.update(kwargs)
        return payload

    async def _trigger(self, payload: Dict[str, Any]):
        async with self.session.post(
            url=Config.ApiUrl.interactions,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.setting["user_token"],
            },
            json=payload,
        ) as resp:
            if not resp.ok:
                return None
            return True

    async def generate(self, prompt: str):
        payload = self._trigger_payload(
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

    async def upscale(self, index: int, msg_id: str, msg_hash: str):
        kwargs = {
            "message_flags": 0,
            "message_id": msg_id,
        }
        payload = self._trigger_payload(
            3,
            {
                "component_type": 2,
                "custom_id": f"MJ::JOB::upsample::{index}::{msg_hash}",
            },
            **kwargs,
        )
        return await self._trigger(payload)

    async def variation(self, index: int, msg_id: str, msg_hash: str):
        kwargs = {
            "message_flags": 0,
            "message_id": msg_id,
        }
        payload = self._trigger_payload(
            3,
            {
                "component_type": 2,
                "custom_id": f"MJ::JOB::variation::{index}::{msg_hash}",
            },
            **kwargs,
        )
        return await self._trigger(payload)

    async def reset(self, msg_id: str, msg_hash: str):
        kwargs = {
            "message_flags": 0,
            "message_id": msg_id,
        }
        payload = self._trigger_payload(
            3,
            {"component_type": 2, "custom_id": f"MJ::JOB::reroll::0::{msg_hash}::SOLO"},
            **kwargs,
        )
        return await self._trigger(payload)

    async def max_upscale(self, msg_id: str, msg_hash: str):
        kwargs = {
            "message_flags": 0,
            "message_id": msg_id,
        }
        payload = self._trigger_payload(
            3,
            {
                "component_type": 2,
                "custom_id": f"MJ::JOB::upsample_max::1::{msg_hash}::SOLO",
            },
            **kwargs,
        )
        return await self._trigger(payload)


if __name__ == "__main__":
    import asyncio
    import aiohttp

    async def main():
        async with aiohttp.ClientSession() as session:
            await Discord(session, Config.Discord.user_token).join_guild(
                Config.Discord.guild_id
            )

    asyncio.run(main())
