from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from models.db.models import db
from models.db.models import SessionLocal, Task


def save_to_db(task_db_obj: Task) -> None:
    """
    Save the task to the database
    Args:
        task_db_obj: Task object
    Returns:
        None
    """
    try:
        db.add(task_db_obj)
        db.commit()
        db.refresh(task_db_obj)
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()


def update_task(task_id: str, message: str):
    """
    Update the task in the database
    Args:
        task_id: Task ID
        message: Message to be updated
    Returns:
        None
    """
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.task_id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        task.message = message  # type: ignore
        db.commit()
        return {"message": "Task updated successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()
