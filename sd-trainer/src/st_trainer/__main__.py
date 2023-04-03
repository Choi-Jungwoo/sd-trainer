import asyncio
import sys

import uvicorn


class ProactorServer(uvicorn.Server):
    def run(self, sockets=None):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.serve(sockets=sockets))


if __name__ == '__main__':
    config = uvicorn.Config('st_trainer.server:app', host='0.0.0.0', port=5000, log_level='info', reload=True)
    server = ProactorServer(config=config) if sys.platform == 'win32' else uvicorn.Server(config=config)
    server.run()
