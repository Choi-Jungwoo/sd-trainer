import uvicorn
from fastapi import FastAPI

from st_trainer.logger import logger

app = FastAPI()


@app.get('/hello')
async def hello():
    logger.info('Hello World!')
    return 'world'


def run_server():
    uvicorn.run('st_trainer.server:app', host='0.0.0.0', port=5000, log_level='info', reload=True)
