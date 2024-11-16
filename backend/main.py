from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend.models import Cupcake, Order
import os
import sqlite3

app = FastAPI()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def initialize_database():
    if not os.path.exists("database.db"):  # Check if the database file exists
        print("Initializing the database...")
        with sqlite3.connect("database.db") as conn:
            with open("backend/database.sql", "r") as f:
                conn.executescript(f.read())
        print("Database initialized.")


# Pydantic Models
class CupcakeSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True

class CartItemSchema(BaseModel):
    id: int
    cupcake_id: int

    class Config:
        orm_mode = True

# Endpoints
@app.get("/api/cupcakes", response_model=list[CupcakeSchema])
def get_cupcakes(db: Session = Depends(get_db)):
    return db.query(Cupcake).all()

@app.post("/api/cart")
def add_to_cart(cupcake_id: int, db: Session = Depends(get_db)):
    cart_item = db.execute("INSERT INTO cart (cupcake_id) VALUES (:cupcake_id)", {"cupcake_id": cupcake_id})
    db.commit()
    return {"message": "Cupcake added to cart"}

@app.get("/api/cart", response_model=list[CartItemSchema])
def get_cart_items(db: Session = Depends(get_db)):
    items = db.execute("SELECT * FROM cart").fetchall()
    return [{"id": item["id"], "cupcake_id": item["cupcake_id"]} for item in items]

@app.delete("/api/cart/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    db.execute("DELETE FROM cart WHERE id = :id", {"id": item_id})
    db.commit()
    return {"message": "Item removed from cart"}

@app.post("/api/orders")
def place_order(db: Session = Depends(get_db)):
    db.execute("DELETE FROM cart")
    db.commit()
    return {"message": "Order placed successfully"}

@app.post("/api/orders/cancel")
def cancel_order(db: Session = Depends(get_db)):
    db.execute("DELETE FROM cart")
    db.commit()
    return {"message": "Order canceled"}
