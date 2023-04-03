import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator

from st_trainer.trainer.process import TrainerProcess


class Status(str, Enum):
    Waiting = 'WAITING'
    Training = 'TRAINING'
    Done = 'DONE'


class TrainerProcessModel(BaseModel):
    name: str
    pid: Optional[int] = None
    exec_name: str
    args: list[str] = []
    log: str


class TrainerTask(BaseModel):
    trainer_process: TrainerProcess = None
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: Optional[str] = None
    status: Status = Status.Waiting
    args: list[str] = []
    pid: Optional[int] = None
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    done_date: Optional[datetime] = None
    start_train_date: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        fields = {
            'trainer_process': {
                'exclude': ...
            }
        }

    @validator('pid', pre=True, always=True, each_item=True)
    def parse_pid(cls, _, values):
        trainer_process = values['trainer_process']
        return trainer_process.pid if trainer_process else None

    @property
    def run(self):
        return self.trainer_process.run
