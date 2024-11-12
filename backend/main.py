from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import sqlite3
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Cupcake, Order

app = FastAPI()

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Models
class Cupcake(BaseModel):
    id: int
    name: str
    description: str
    price: float

class CartItem(BaseModel):
    id: int
    cupcake_id: int

# Endpoints
@app.get("/api/cupcakes", response_model=List[Cupcake])
def get_cupcakes():
    conn = get_db_connection()
    cupcakes = conn.execute('SELECT * FROM cupcakes').fetchall()
    return [{"id": cupcake["id"], "name": cupcake["name"], "description": cupcake["description"], "price": cupcake["price"]} for cupcake in cupcakes]

@app.post("/api/cart")
def add_to_cart(cupcake_id: int):
    conn = get_db_connection()
    conn.execute('INSERT INTO cart (cupcake_id) VALUES (?)', (cupcake_id,))
    conn.commit()
    conn.close()
    return {"message": "Cupcake added to cart"}

@app.get("/api/cart", response_model=List[CartItem])
def get_cart_items():
    conn = get_db_connection()
    cart_items = conn.execute('SELECT * FROM cart').fetchall()
    return [{"id": item["id"], "cupcake_id": item["cupcake_id"]} for item in cart_items]

@app.delete("/api/cart/{item_id}")
def remove_from_cart(item_id: int):
    conn = get_db_connection()
    conn.execute('DELETE FROM cart WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item removed from cart"}

@app.post("/api/orders")
def place_order():
    conn = get_db_connection()
    conn.execute("INSERT INTO orders (status) VALUES ('completed')")
    conn.commit()
    conn.close()
    return {"message": "Order placed successfully"}

@app.post("/api/orders/cancel")
def cancel_order():
    conn = get_db_connection()
    conn.execute("DELETE FROM cart")
    conn.commit()
    conn.close()
    return {"message": "Order canceled"}
