import re
from typing import Union
from loguru import logger

from discord import Intents, Message
from discord.ext import commands

from config import Config

from app.database import async_session, Trigger, TriggerStatus, TriggerDAL

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)


def match_trigger_id(message: Message) -> Union[int, None]:
    if message.author.id != 936929561302675456:
        return None
    match = re.findall(
        f"{Config.Prompt.prefix}(\w+?){Config.Prompt.suffix}", message.content
    )
    return int(match[0]) if match else None


def match_percent(s: str) -> Union[int, None]:
    match = re.findall(r"(\d+)(?=%)", s)
    return int(match[0]) if match else None


@bot.event
async def on_ready():
    logger.success(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message: Message):
    trigger_id = match_trigger_id(message)
    if not trigger_id:
        return
    async with async_session() as session:
        logger.info(f"{trigger_id} content: {message.content}")

        content_lower = message.content.lower()
        if "waiting to start" in content_lower:
            trigger_status = TriggerStatus.pending.value
        elif "(stopped)" in content_lower:
            trigger_status = TriggerStatus.failed.value
        else:
            trigger_status = TriggerStatus.success.value

        async with session.begin():
            await TriggerDAL(session).update_status(trigger_id, trigger_status)

        if message.attachments:
            image = message.attachments[0]
            if not (image.width and image.height):
                return

            logger.debug(f"attachments: {message.attachments[0].url}")

            async with session.begin():
                trigger: Trigger = await TriggerDAL(session).get(trigger_id)
                if trigger:
                    trigger.percent = 100
                    trigger.filename = image.filename
                    trigger.image_url = image.url

                    trigger.status = TriggerStatus.success

                    trigger.message_id = str(message.id)
                    trigger.message_hash = str(hash(message))
                    await session.commit()


@bot.event
async def on_message_edit(_: Message, after: Message):
    trigger_id = match_trigger_id(after)
    if not trigger_id:
        return

    async with async_session() as session:
        logger.info(f"{trigger_id} content: {after.content}")

        if after.attachments:
            image = after.attachments[0]
            if not (image.width and image.height):
                return
            percent = match_percent(after.content)

            logger.debug(f"attachments: {after.attachments[0].url}")

            async with session.begin():
                trigger: Trigger = await TriggerDAL(session).get(trigger_id)
                if trigger:
                    if trigger.status == TriggerStatus.pending:
                        trigger.status = TriggerStatus.generating
                    if percent:
                        trigger.percent = percent
                    trigger.image_url = image.url
                    await session.commit()


@bot.event
async def on_message_delete(message: Message):
    trigger_id = match_trigger_id(message)
    if not trigger_id:
        return

    # if message.attachments:
    #     image = message.attachments[0]
    #     if not (image.width and image.height):
    #         return
    #
    #     async with session.begin():
    #         trigger: Trigger = await TriggerDAL(session).get(trigger_id)
    #         if trigger:
    #             trigger.percent = 100
    #             trigger.filename = image.filename
    #             trigger.image_url = image.url
    #             trigger.message_id = image.id
    #             trigger.status = TriggerStatus.end
    #             await session.commit()
