# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, crud, schemas
from database import engine, Base, get_db
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Auto-create tables
Base.metadata.create_all(bind=engine)

# API Endpoints
@app.get("/currencies", response_model=list[schemas.CurrencyResponse])
def get_currencies(db: Session = Depends(get_db)):
    return crud.get_all_currencies(db)

@app.get("/currencies/{currency_id}", response_model=schemas.CurrencyResponse)
def get_currency(currency_id: int, db: Session = Depends(get_db)):
    currency = crud.get_currency_by_id(db, currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency

@app.post("/currencies", response_model=schemas.CurrencyResponse)
def create_currency(currency: schemas.CurrencyCreate, db: Session = Depends(get_db)):
    return crud.create_currency(db, currency)

@app.post("/currencies/bulk")
def create_bulk_currency(currencies: list[schemas.CurrencyCreate], db: Session = Depends(get_db)):
    return crud.create_or_update_bulk_currencies(db, currencies)

@app.put("/currencies/{currency_id}", response_model=schemas.CurrencyResponse)
def update_currency(currency_id: int, updates: schemas.CurrencyUpdate, db: Session = Depends(get_db)):
    updated_currency = crud.update_currency(db, currency_id, updates)
    if not updated_currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return updated_currency

@app.delete("/currencies/{currency_id}", response_model=schemas.CurrencyResponse)
def delete_currency(currency_id: int, db: Session = Depends(get_db)):
    deleted_currency = crud.delete_currency(db, currency_id)
    if not deleted_currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return deleted_currency