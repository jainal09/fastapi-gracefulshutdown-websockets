from pydantic import BaseModel


class TaskOut(BaseModel):
    id: int
    task_id: str
    message: str


class QueueOut(BaseModel):
    task_lenth: int
