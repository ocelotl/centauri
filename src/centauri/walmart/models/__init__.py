from pydantic import BaseModel


class Quantity(BaseModel):
    unit: str
    amount: int


class Inventory(BaseModel):
    sku: str
    quantity: Quantity
