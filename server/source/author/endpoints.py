from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends

from source.author.schemas import Author as AuthorSchema
from source.author.schemas import AuthorCreate, AuthorUpdate
from source.author.service import author_service
from source.exceptions import ValidationErrorResponse
from source.models.author import Author
from source.postgres import AsyncSession, get_db_session

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/", summary="List authors", response_model=list[AuthorSchema])
async def list(
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    return await author_service.list(session)


@router.get("/{id}", summary="Get an author", response_model=AuthorSchema)
async def get(id: UUID, session: AsyncSession = Depends(get_db_session)) -> Any:
    return await author_service.get(session, id)


@router.post(
    "/",
    summary="Create an author",
    responses={
        422: {"model": ValidationErrorResponse, "description": "Validation Error"}
    },
    response_model=AuthorSchema,
)
async def create(
    author_create: AuthorCreate, session: AsyncSession = Depends(get_db_session)
) -> Author:
    return await author_service.create(session, author_create)


@router.patch(
    "/{id}",
    summary="Update an author",
    responses={
        422: {"model": ValidationErrorResponse, "description": "Validation Error"}
    },
    response_model=AuthorSchema,
)
async def update(
    id: UUID,
    author_update: AuthorUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> Author:
    return await author_service.update(session, id, author_update)
