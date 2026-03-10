from fastapi import APIRouter

from source.author.endpoints import router as author_router

router = APIRouter(prefix="/v1")

# /authors
router.include_router(author_router)
