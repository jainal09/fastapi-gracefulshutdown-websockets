from pydantic import BaseModel


class TaskOut(BaseModel):
    """
    TaskOut: Pydantic model for sending the Response of the Task
    """
    id: int
    task_id: str
    message: str


class QueueOut(BaseModel):
    """
    QueueOut: Pydantic model for sending the Response of the Queue
    """
    task_lenth: int
