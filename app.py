from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ItemBase(BaseModel):
    name: str
    price: float


class Item(ItemBase):
    id: int


class ItemCreate(ItemBase):
    pass


# In-memory storage with seed data (survives until process restarts)
items: list[Item] = [
    Item(id=1, name="Phone", price=1009.99),
    Item(id=2, name="Tablet", price=190.50),
    Item(id=3, name="Laptop", price=4234.25),
]
_next_id = 4


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/items")
def get_items():
    return {"items": items}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for it in items:
        if it.id == item_id:
            return it
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items")
def create_item(item: ItemCreate):
    global _next_id
    new_item = Item(id=_next_id, name=item.name, price=item.price)
    _next_id += 1
    items.append(new_item)
    return {
        "message": "Item added successfully!",
        "item": new_item,
    }
