import os
from dotenv import load_dotenv

load_dotenv()


def getenv(key: str, default=None, required: bool = False):
    value = os.getenv(key, default)
    if required and not value:
        raise Exception(f"Missing required environment variable: [{key}]")
    return value


def async_database_url(url: str) -> str:
    return url.replace("postgre://", "postgresql://").replace(
        "postgresql://", "postgresql+asyncpg://"
    )


class Config:
    # Runtime
    base_url = os.path.dirname(os.path.abspath(__file__))
    environment = getenv("ENVIRONMENT") if getenv("ENVIRONMENT") else "DEVELOPMENT"
    http_proxy = getenv("HTTP_PROXY")
    secret = getenv("SECRET")
    public = getenv("PUBLIC", default=False)

    database_url = async_database_url(
        getenv("DATABASE_URL", "sqlite+aiosqlite:///./tmp.db")
    )

    class Prompt:
        prefix = "<#"
        suffix = "#>"

    class Discord:
        user_token = getenv("USER_TOKEN", required=True)
        bot_token = getenv("BOT_TOKEN", required=True)
        guild_id = getenv("GUILD_ID", required=True)
        channel_id = getenv("CHANNEL_ID", required=True)

    class ApiUrl:
        interactions = "https://discord.com/api/v9/interactions"
        upload_attachment = (
            f"https://discord.com/api/v9/channels/{getenv('CHANNEL_ID')}/attachments"
        )
        send_message = (
            f"https://discord.com/api/v9/channels/{getenv('CHANNEL_ID')}/messages"
        )
