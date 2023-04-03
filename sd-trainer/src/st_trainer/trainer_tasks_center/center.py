import asyncio
import datetime

from st_trainer.trainer.process import TrainerProcess
from st_trainer.trainer_tasks_center.trainer_task import TrainerTask, Status

MAX_TRAINING_COUNT = 1


class TrainerTasksCenter:
    __tasks: list[TrainerTask] = []

    @staticmethod
    async def push_task(trainer_task: TrainerTask):
        TrainerTasksCenter.__tasks.append(trainer_task)
        await TrainerTasksCenter.__start_waiting_tasks()

    @staticmethod
    async def get_tasks():
        return TrainerTasksCenter.__tasks

    @staticmethod
    async def __start_waiting_tasks():
        training_task_len = len([task for task in TrainerTasksCenter.__tasks if task.status == Status.Training])

        if not training_task_len < MAX_TRAINING_COUNT:
            return

        waiting_tasks = [task for task in TrainerTasksCenter.__tasks if task.status == Status.Waiting]
        for task in waiting_tasks[0:MAX_TRAINING_COUNT]:
            asyncio.create_task(task.run())

            # init
            task.status = Status.Training
            task.start_train_date = datetime.datetime.now(datetime.timezone.utc)
            task.name = task.trainer_process.name

            # bind callback
            task.trainer_process.exit_callbacks = TrainerTasksCenter.__exit_callback

    @staticmethod
    async def __exit_callback(process: TrainerProcess, _: int):
        tasks = [task for task in TrainerTasksCenter.__tasks if task.pid == process.pid]
        task = tasks[0] if tasks else None

        if not task:
            return

        task.status = Status.Done
        task.done_date = datetime.datetime.now(datetime.timezone.utc)

        await TrainerTasksCenter.__start_waiting_tasks()
