from __future__ import annotations

from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.sql.base import ExecutableOption

from source.kit.utils import utc_now

from .db.models import RecordModel
from .db.postgres import AsyncSession


class ResourceServiceReader[ModelType: RecordModel]:
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get(
        self,
        session: AsyncSession,
        id: UUID,
        allow_deleted: bool = False,
        *,
        options: Sequence[ExecutableOption] | None = None,
    ) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        if not allow_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        if options is not None:
            query = query.options(*options)
        res = await session.execute(query)
        return res.scalars().unique().one_or_none()

    async def get_by(self, session: AsyncSession, **clauses: Any) -> ModelType | None:
        query = select(self.model).filter_by(**clauses)
        res = await session.execute(query)
        return res.scalars().unique().one_or_none()

    async def soft_delete(self, session: AsyncSession, id: UUID) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == id, self.model.deleted_at.is_(None))
            .values(
                deleted_at=utc_now(),
            )
        )
        await session.execute(stmt)
        await session.flush()
