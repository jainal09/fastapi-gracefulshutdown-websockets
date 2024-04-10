import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from models.api.models import QueueOut, TaskOut
from models.db.models import SessionLocal, TaskModel
from services.db_ops.flag_ops import read_flag
from settings import settings_config
from tasks.bg_tasks import process_task, queue_task, remove_task

router = APIRouter()
queue = settings_config.queue


@router.get("/health")
async def health() -> JSONResponse:
    """
    Health check for the server
    Args:
        None
    Returns:
        JSONResponse: JSON response
    """
    if read_flag():
        return JSONResponse(status_code=200, content={"status": "ok"})
    else:
        return JSONResponse(
            status_code=503, content={"status": "Service Under Graceful Shutdown"}
        )


@router.post("/create-task/")
async def create_task(background_tasks: BackgroundTasks) -> dict:
    """
    Create a task and add it to the queue
    Args:
        background_tasks: BackgroundTasks
    Returns:
        dict: Response message
    """
    if not read_flag():
        raise HTTPException(status_code=503, detail="Service Under Graceful Shutdown")
    task_id = str(uuid.uuid4())
    queue_task(task_id=task_id)
    print("🚀 Background process started 🚀")
    background_tasks.add_task(process_task, task_id=task_id,
                              message=f"Task {task_id} processed")
    background_tasks.add_task(remove_task, task_id=task_id)
    queue.append(task_id)
    return {"message": f"Task {task_id} Queued"}


@router.get("/tasks/{task_id}", response_model=TaskOut)
async def read_task_by_id(task_id: str): # type: ignore
    """
    Get Status of a Task
    Args:
        task_id: Task ID
    Returns:
        TaskOut: Task object
    """
    db = SessionLocal()
    try:
        task = db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return JSONResponse(
            {"task_id": task.__dict__["task_id"], "message": task.__dict__["message"]},
        )
    finally:
        db.close()


@router.get("/get_queue_length/", response_model=QueueOut)
async def read_task():
    """
    Get the length of the queue
    Args:
        None
    Returns:
        QueueOut: Queue object
    """
    return QueueOut(task_lenth=len(queue))
