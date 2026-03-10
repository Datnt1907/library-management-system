from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from source.postgres import AsyncSession, get_db_session

router = APIRouter(tags=["health"], include_in_schema=True)


@router.get("/health")
async def health(session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    try:
        await session.execute(select(1))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Database is not available") from e

    return {"status": "ok"}
