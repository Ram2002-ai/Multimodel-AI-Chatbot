"""Initialize database tables and run first superuser creation (if needed)."""

from app.database.base import Base
from app.database.session import engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)