import asyncio

from fastapi import FastAPI

from st_trainer.api import router as api_router
from st_trainer.logger import logger

app = FastAPI(
    title='SD Trainer',
)
app.include_router(api_router)


@app.on_event('startup')
async def on_start():
    logger.info(asyncio.get_event_loop())
