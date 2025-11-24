from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime

from database import SessionLocal, engine, Base
from models import Subscription
from schemas import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from email_parser import EmailParser

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Subscription Manager API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Subscription Manager API"}

@app.get("/api/subscriptions", response_model=List[SubscriptionResponse])
def get_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all subscriptions"""
    subscriptions = db.query(Subscription).offset(skip).limit(limit).all()
    return subscriptions

@app.get("/api/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Get a specific subscription"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@app.post("/api/subscriptions", response_model=SubscriptionResponse)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    """Create a new subscription"""
    db_subscription = Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@app.put("/api/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: int, 
    subscription: SubscriptionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a subscription"""
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    update_data = subscription.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_subscription, field, value)
    
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@app.delete("/api/subscriptions/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Delete/cancel a subscription"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(subscription)
    db.commit()
    return {"message": "Subscription cancelled successfully"}

@app.post("/api/subscriptions/discover")
def discover_subscriptions(db: Session = Depends(get_db)):
    """Automatically discover subscriptions from email"""
    parser = EmailParser()
    discovered = parser.discover_subscriptions()
    
    # Add discovered subscriptions to database
    added_count = 0
    for sub_data in discovered:
        # Check if subscription already exists
        existing = db.query(Subscription).filter(
            Subscription.company == sub_data.get("company"),
            Subscription.email == sub_data.get("email")
        ).first()
        
        if not existing:
            db_subscription = Subscription(**sub_data)
            db.add(db_subscription)
            added_count += 1
    
    db.commit()
    return {"message": f"Discovered {added_count} new subscriptions", "total": len(discovered)}

@app.get("/api/subscriptions/stats/summary")
def get_stats(db: Session = Depends(get_db)):
    """Get subscription statistics"""
    subscriptions = db.query(Subscription).all()
    total_monthly = sum(sub.monthly_cost for sub in subscriptions if sub.monthly_cost)
    total_yearly = sum(sub.yearly_cost for sub in subscriptions if sub.yearly_cost)
    
    return {
        "total_subscriptions": len(subscriptions),
        "total_monthly_cost": total_monthly,
        "total_yearly_cost": total_yearly,
        "estimated_yearly": total_monthly * 12 if total_monthly else 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

