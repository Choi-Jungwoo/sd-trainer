from fastapi import APIRouter

from .train import router as train_route

router = APIRouter(
    prefix='/lora',
    tags=['lora'],
)

router.include_router(train_route)
