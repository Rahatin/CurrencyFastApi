from sqlalchemy.orm import Session
from models import Currency
from schemas import CurrencyCreate, CurrencyUpdate
from sqlalchemy.exc import IntegrityError

def get_all_currencies(db: Session):
    return db.query(Currency).all()

def get_currency_by_id(db: Session, currency_id: int):
    return db.query(Currency).filter(Currency.id == currency_id).first()

def create_currency(db: Session, currency_data: CurrencyCreate):
    db_currency = Currency(**currency_data.dict())
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency
#
# def create_bulk_currencies(db: Session, currency_list):
#     db.bulk_insert_mappings(Currency, [currency.dict() for currency in currency_list])
#     db.commit()
#     return {"message": "Currencies added successfully"}

def create_or_update_bulk_currencies(db: Session, currency_list):
    for currency_data in currency_list:
        currency_dict = currency_data.dict()
        existing_currency = db.query(Currency).filter(Currency.country == currency_dict["country"]).first()

        if existing_currency:
            # Update existing currency
            for key, value in currency_dict.items():
                setattr(existing_currency, key, value)
        else:
            # Insert new currency
            new_currency = Currency(**currency_dict)
            db.add(new_currency)

    try:
        db.commit()
        return {"message": "Currencies processed successfully"}
    except IntegrityError:
        db.rollback()
        return {"error": "Database integrity error. Check your data."}

def update_currency(db: Session, currency_id: int, updates: CurrencyUpdate):
    db_currency = db.query(Currency).filter(Currency.id == currency_id).first()
    if not db_currency:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_currency, key, value)
    db.commit()
    db.refresh(db_currency)
    return db_currency
