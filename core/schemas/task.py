from pydantic import BaseModel, ConfigDict

from core.schemas.category import CategoryRead


class TaskBase(BaseModel):
    title: str
    pomodoro_count: int
    category: int


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(TaskCreate):
    pass


class TaskUpdatePartial(BaseModel):
    title: str | None = None
    pomodoro_count: int | None = None
    category: int | None = None