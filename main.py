from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.database import SessionLocal
from backend.models import Cupcake, Order
from pydantic import BaseModel
import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database using lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists("database.db"):  # Check if the database file exists
        print("Initializing the database...")
        with sqlite3.connect("database.db") as conn:
            with open("backend/database.sql", "r") as f:
                conn.executescript(f.read())
        print("Database initialized.")
    yield  # This allows the application to run

# Configure FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CupcakeSchema(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float

    class Config:
        from_attributes = True

class CartItemSchema(BaseModel):
    id: int
    cupcake_id: int
    cupcake: CupcakeSchema

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    id: int
    status: str
    cupcake_id: int

    class Config:
        from_attributes = True

class CartItem(BaseModel):
    cupcake_id: int

app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).parent / "frontend" / "static")),
    name="static",
)

static_path = Path(__file__).parent / "frontend" / "static"
if not static_path.exists():
    raise RuntimeError(f"Static files directory does not exist: {static_path}")

# API Endpoints
@app.get("/api/cupcakes", response_model=list[CupcakeSchema])
def get_cupcakes(db: Session = Depends(get_db)):
    return db.query(Cupcake).all()

@app.post("/api/cart")
def add_to_cart(cart_item: CartItem, db: Session = Depends(get_db)):
    db.execute(text("INSERT INTO cart (cupcake_id) VALUES (:cupcake_id)"), {"cupcake_id": cart_item.cupcake_id})
    db.commit()
    return {"message": "Cupcake added to cart"}

@app.get("/api/cart", response_model=list[CartItemSchema])
def get_cart_items(db: Session = Depends(get_db)):
    items = db.execute(
        text("""
            SELECT cart.id, cart.cupcake_id, cupcakes.id, cupcakes.nome, cupcakes.descricao, cupcakes.preco
            FROM cart
            JOIN cupcakes ON cart.cupcake_id = cupcakes.id
        """)
    ).fetchall()

    return [
        {
            "id": item[0],
            "cupcake_id": item[1],
            "cupcake": {
                "id": item[2],
                "nome": item[3],
                "descricao": item[4],
                "preco": item[5],
            }
        }
        for item in items
    ]

@app.delete("/api/cart/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM cart WHERE id = :id"), {"id": item_id})
    db.commit()
    return {"message": "Item removed from cart"}

@app.post("/api/orders")
def place_order(db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM cart"))
    db.commit()
    return {"message": "Order placed successfully and database reset"}

@app.post("/api/orders/cancel")
def cancel_order(db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM cart"))
    db.commit()
    return {"message": "Order canceled and database reset"}

# Frontend Routes
@app.get("/", response_class=HTMLResponse)
def serve_home():
    with open("frontend/templates/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)
