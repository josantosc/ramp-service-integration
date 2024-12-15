from typing import List

from sqlmodel import SQLModel, Field, Relationship


class ItemBase(SQLModel):
    title: str
    description: str = None # type: ignore


class ItemCreate(ItemBase):
    title: str


class ItemUpdate(ItemBase):
    title: str = None  # type: ignore


class Item(SQLModel, table=True):
    __tablename__ = 'item'
    id: int = Field(default=None, primary_key=True)
    title: str
    #owner_id: int = Field(default=None, foreign_key="users.id")
    #owner: 'Users' = Relationship(back_populates="item")


class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: List[ItemPublic]
    count: int
