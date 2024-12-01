

from sqlalchemy import select as sa_select
from database import Task0rm, new_session
from schemas import STaskAdd, STask

class TaskRepository:
    @classmethod
    async def add_task(cls, task: STaskAdd) -> int:
        async with new_session() as session:
            data = task.model_dump()  
            new_task = Task0rm(**data)
            session.add(new_task)
            await session.commit()  
            return new_task.id

    @classmethod
    async def get_tasks(cls) -> list[STask]:
        async with new_session() as session:
            query = sa_select(Task0rm)  # Используем переименованный импорт
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks = [STask.model_validate(task_model) for task_model in task_models]  # Pydantic v2
            return tasks
