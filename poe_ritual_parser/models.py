from pydantic import BaseModel


class Item(BaseModel):
    cost: int
    item_class: str
    rarity: str
