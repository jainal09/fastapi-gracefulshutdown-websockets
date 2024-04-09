import asyncio
import time

from models.db.models import Task
from services.db_ops.task_ops import save_to_db, update_task
from settings import settings_config

manager = settings_config.manager


queue = settings_config.queue


async def process_task(task_id: str, message: str) -> None:
    """
    Process the task in the background
    Args:
        task_id: Task ID
        message: Message to be sent
    Returns:
        None
    """
    await asyncio.sleep(20)  # Simulate a long running task
    print("🚀 Background process Called 🚀")
    update_task(task_id=task_id, message=message)
    print("🚀 Background process Completed 🚀")
    await manager.send_socket_message(f"{task_id} {message}")


def remove_task(task_id: str) -> None:
    """
    Remove the task from the queue
    Args:
        task_id: Task ID
    Returns:
        None
    """
    queue.remove(task_id)


def queue_task(task_id: str) -> None:
    """
    Queue the task to be processed
    Args:
        task_id: Task ID
    Returns:
        None
    """
    task = Task(task_id=task_id, message=f"Task {task_id} queued")
    save_to_db(task_db_obj=task)
