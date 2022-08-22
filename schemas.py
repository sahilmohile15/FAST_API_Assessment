from typing import List, Optional

from pydantic import BaseModel


class AddBase(BaseModel):
    name: str
    address : str
    address_point: Optional[str] = None


class AddCreate(AddBase):
    pass


class AddGet(AddBase):
    pass


class Address(AddBase):
    id: int

    class Config:
        orm_mode = True

