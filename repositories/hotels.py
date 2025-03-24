from sqlalchemy import select
from repositories.base import BaseRepository
from src.models.hotels import HotelsORM


class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        query = select(HotelsORM)
        if location:
            query = query.where(HotelsORM.location.ilike(f"%{location.strip()}%"))
        if title:
            query = query.where(HotelsORM.title.ilike(f"%{title.strip()}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

