from fastapi import APIRouter, Depends
from pydantic import BaseModel

from repository import TaskRepository
from schemas import STask, STaskAdd

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


class STaskId(BaseModel):
    id: int


@router.post("/")
async def add_task(task: STaskAdd = Depends()) -> STaskId:
    new_task_id = await TaskRepository.add_task(task)
    return {"id": new_task_id}


@router.get("/")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.get_tasks()
    return tasks
