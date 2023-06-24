import aiohttp
from fastapi import APIRouter
from utils import unique_id
from config import Config
from app import schema
from app.lib.discord import MidjourneyBot
from app.database import async_session, TriggerDAL


router = APIRouter()


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
async def imagine(data: schema.ImageGeneration):
    trigger_id = str(unique_id())

    if not data.picurl and data.prompt.startswith(("http://", "https://")):
        picurl, _, prompt = data.prompt.partition(" ")

    prompt = f"{data.picurl + ' ' if data.picurl else ''}{Config.Prompt.prefix}{trigger_id}{Config.Prompt.suffix}{data.prompt}"
    async with async_session() as session:
        async with session.begin():
            await TriggerDAL(session).new(_id=int(trigger_id), prompt=prompt)

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
    ) as session:
        await MidjourneyBot(session).generate(prompt)

    return {"trigger_id": trigger_id, "trigger_type": "generate"}
