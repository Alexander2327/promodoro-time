from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    pomodoro_count: int
    category_id: int


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
