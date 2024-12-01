import select
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
import greenlet
from database import Task0rm, new_session
from router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова")
    yield
    print("выключение")


app = FastAPI(lifespan=lifespan)


class STaskAdd(BaseModel):
    name: str
    description: Optional[str] = None


class STask(STaskAdd):
    id: int



tasks = []



@app.post("/task")
async def add_task(task: STaskAdd = Depends()):
   return {"data": task}



async def add_task(data: dict) -> int:
   async with new_session() as session:
       new_task = Task0rm(**data)
       session.add(new_task)
       await session.flush()
       await session.commit()
       return new_task.id

async def get_tasks():
   async with new_session() as session:
       query = select(Task0rm)
       result = await session.execute(query)
       task_models = result.scalars().all()
       return task_models






app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)