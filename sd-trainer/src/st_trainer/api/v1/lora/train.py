from fastapi import APIRouter

from st_trainer.trainer.lora import LoraTrainerProcess
from st_trainer.trainer_tasks_center.center import TrainerTasksCenter
from st_trainer.trainer_tasks_center.trainer_task import TrainerTask

router = APIRouter(
    prefix='/train',
    tags=['train']
)


@router.get('/')
async def train_tasks():
    return await TrainerTasksCenter.get_tasks()


@router.post('/')
async def start_train():
    task = TrainerTask(trainer_process=LoraTrainerProcess())
    await TrainerTasksCenter.push_task(task)

    return task
