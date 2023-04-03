from fastapi import APIRouter

from .lora import router as lora_router

router = APIRouter(
    prefix='/v1',
    tags=['v1']
)

router.include_router(lora_router)
