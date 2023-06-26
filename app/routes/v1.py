import json

import aiohttp
from typing import Dict
from fastapi import APIRouter, Depends, Request
from utils import unique_id
from config import Config
from app import schema
from app.lib.discord import MidjourneyBot, Discord
from app.database import async_session, TriggerDAL
from utils.fastapi import get_setting

router = APIRouter()


async def join_guild(user_token: str):
    async with aiohttp.ClientSession() as session:
        discord = Discord(session, user_token)
        await discord.join_guild(Config.Discord.guild_id)


@router.get("/trigger")
async def trigger(id: int):
    async with async_session() as session:
        async with session.begin():
            trigger = await TriggerDAL(session).get(id)

    return {
        "id": trigger.id,
        "type": trigger.type,
        "status": trigger.status,
        "percent": trigger.percent,
        "message_id": trigger.message_id,
        "filename": trigger.filename,
        "image_url": trigger.image_url,
        "created_at": trigger.created_at,
        "updated_at": trigger.updated_at,
    }


@router.post("/imagine", response_model=schema.ImageGenerationResponse)
async def imagine(data: schema.ImageGeneration, setting: Dict = Depends(get_setting)):
    trigger_id = str(unique_id())

    if not data.picurl and data.prompt.startswith(("http://", "https://")):
        picurl, _, prompt = data.prompt.partition(" ")

    prompt = f"{data.picurl + ' ' if data.picurl else ''}{Config.Prompt.prefix}{trigger_id}{Config.Prompt.suffix}{data.prompt}"
    async with async_session() as session:
        async with session.begin():
            await TriggerDAL(session).new(
                _id=int(trigger_id), payload=json.dumps({"prompt": data.prompt})
            )

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
    ) as session:
        await MidjourneyBot(session, setting).generate(prompt)

    return {"trigger_id": trigger_id, "trigger_type": "generate"}


@router.post("/upscale", response_model=schema.ImageGenerationResponse)
@router.post("/variation", response_model=schema.ImageGenerationResponse)
async def upscale(
    data: schema.ImageUVR, request: Request, setting: Dict = Depends(get_setting)
):
    trigger_id = data.trigger_id
    trigger_type = "upscale" if "upscale" in request.url.path else "variation"

    async with async_session() as session:
        async with session.begin():
            trigger = await TriggerDAL(session).get(_id=int(trigger_id))
            new_tigger = await TriggerDAL(session).new(
                _id=int(trigger_id), status=trigger_type
            )

    msg_id = trigger.message_id
    msg_hash = trigger.message_hash

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
    ) as session:
        match trigger_type:
            case "upscale":
                await MidjourneyBot(session, setting).upscale(
                    data.index, msg_id, msg_hash
                )
            case "variation":
                await MidjourneyBot(session, setting).variation(
                    data.index, msg_id, msg_hash
                )

    return {"trigger_id": new_tigger.id, "trigger_type": trigger_type}


@router.post("/reset", response_model=schema.ImageGenerationResponse)
async def reset(data: schema.ImageUVR):
    trigger_id = data.trigger_id
    trigger_type = "reset"

    return {"trigger_id": trigger_id, "trigger_type": trigger_type}
