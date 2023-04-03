import asyncio
from asyncio import StreamReader
from asyncio.subprocess import Process
from typing import Optional, Callable, Awaitable, Any

from st_trainer.logger import logger


class TrainerProcess:
    def __init__(
            self,
            name: str,
            exec_name: str,
            *,
            args: Optional[list[str]] = None,
    ):
        self.__proc: Optional[Process] = None
        self.__log = ''
        self.name = name
        self.exec_name = exec_name
        self.args = args
        self.out_callbacks: list[Callable[[Any, str], Awaitable[None]]] = []
        self.err_callbacks: list[Callable[[Any, str], Awaitable[None]]] = []
        self.exit_callbacks: list[Callable[[Any, int], Awaitable[None]]] = []
        self.start_callbacks: list[Callable[[Any], Awaitable[None]]] = []

    @property
    def log(self):
        return self.__log

    @property
    def pid(self):
        return self.proc.pid if self.proc else None

    @property
    def proc(self) -> Process:
        return self.__proc

    async def run(self):
        proc = await asyncio.create_subprocess_exec(
            self.exec_name,
            *(self.args if self.args else []),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self.__proc = proc

        for callback in self.start_callbacks:
            await callback(self)

        logger.info(f'trainer process [{self.pid}] {self.name} start training!')

        await asyncio.wait([
            asyncio.create_task(TrainerProcess.__read_line(proc.stdout, self.__out_callback)),
            asyncio.create_task(TrainerProcess.__read_line(proc.stderr, self.__err_callback))
        ])
        code = await proc.wait()

        await self.__exit_callback(code)

        logger.info(f'trainer process [{self.pid}] {self.name} exited.')

    @staticmethod
    async def __read_line(stream: StreamReader, callback: Callable[[str], Awaitable[None]]):
        while True:
            line = await stream.readline()
            if not line:
                break
            if callback is not None:
                try:
                    await callback(line.decode('gbk').replace('\n', ''))
                except UnicodeDecodeError:
                    await callback(str(line))

    async def __pipe_callback(self, callbacks, line, level):
        log_func = getattr(logger, level)
        self.__log += f'{line}\n'
        log_func(f'trainer process [{self.pid}] {self.name}: {line}')
        for callback in callbacks:
            await callback(self, line)

    async def __out_callback(self, line):
        await self.__pipe_callback(self.out_callbacks, line, 'debug')

    async def __err_callback(self, line):
        await self.__pipe_callback(self.err_callbacks, line, 'error')

    async def __exit_callback(self, code):
        for callback in self.exit_callbacks:
            await callback(self, code)
        self.__pid = None
