from app.repositories.base import BaseRepository
from app.models.api_key import APIKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class APIKeyRepository(BaseRepository[APIKey]):
    def __init__(self, session: AsyncSession):
        super().__init__(APIKey, session)

    async def get_by_key_hash(self, key_hash: str) -> APIKey | None:
        stmt = select(APIKey).where(APIKey.key_hash == key_hash, APIKey.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()