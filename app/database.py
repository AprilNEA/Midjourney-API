import enum
from typing import Optional
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import Config

engine = create_async_engine(Config.database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class TriggerStatus(enum.Enum):
    pending = "pending"
    start = "start"  # 首次触发 MessageType.chat_input_command
    generating = "generating"  # 生成中
    end = "end"  # 生成结束 MessageType.default
    error = "error"  # 生成错误
    banned = "banned"  # 提示词被禁

    text = "text"  # 文本内容：describe
    verify = "verify"  # 需人工验证


class TriggerType(enum.Enum):
    generate = "generate"
    upscale = "upscale"
    variation = "variation"
    max_upscale = "max_upscale"
    reset = "reset"
    describe = "describe"


class Trigger(Base):
    __tablename__ = "trigger"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[TriggerType] = mapped_column(default=TriggerType.generate, index=True)
    status: Mapped[TriggerStatus] = mapped_column(
        default=TriggerStatus.pending, index=True
    )
    percent: Mapped[int] = mapped_column(default=0)
    prompt: Mapped[str] = mapped_column(index=True)
    filename: Mapped[str] = mapped_column(nullable=True, index=True)
    message_id: Mapped[int] = mapped_column(nullable=True, index=True)
    image_url: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())


class TriggerDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, _id: int) -> Optional[Trigger]:
        q = await self.db.execute(select(Trigger).filter_by(id=_id))
        return q.scalars().first()

    async def new(self, _id: int, **kwargs):
        trigger = Trigger(id=_id, **kwargs)
        self.db.add(trigger)
        await self.db.commit()
        return trigger

    async def update_percent(self, _id: int, percent: int, url: str = None):
        trigger = await self.get(_id)
        trigger.percent = percent
        if url:
            trigger.image_url = url
        await self.db.commit()
        return trigger

    async def update_status(self, _id: int, status: TriggerStatus):
        trigger = await self.get(_id)
        trigger.status = status
        await self.db.commit()
        return trigger

    async def finish(self, _id: int, **kwargs):
        trigger = await self.get(_id)
        trigger.status = TriggerStatus.end
        trigger.percent = 100
        if trigger.type == TriggerType.generate:
            trigger.filename = kwargs.get("filename")
            trigger.message_id = kwargs.get("message_id")
            trigger.image_url = kwargs.get("image_url")

        await self.db.commit()
        return trigger


async def db_startup():
    # create db tables
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":

    async def main():
        async with async_session() as session:
            async with session.begin():
                trigger = await TriggerDAL(session).get(1)
                print(trigger)

    import asyncio

    asyncio.run(db_startup())
    asyncio.run(main())
