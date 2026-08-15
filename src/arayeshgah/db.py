import pathlib
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from arayeshgah import config
from arayeshgah.models import Base

engine = create_async_engine(config.DATABASE_URL, echo=False)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """
    Creates tables automatically.

    For production-grade projects, use Alembic migrations instead.
    For MVP, this is fine.
    """
    backend = engine.url.get_backend_name()

    if backend == "sqlite":
        db_path = pathlib.Path(str(engine.url.database))
        db_path.parent.mkdir(parents=True, exist_ok=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
