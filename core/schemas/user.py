from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserAuth(UserBase):
    id: int


class UserRead(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserUpdatePartial(BaseModel):
    username: str | None = None
    is_active: bool | None = None