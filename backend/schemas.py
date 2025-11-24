from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class SubscriptionBase(BaseModel):
    company: str
    service_name: Optional[str] = None
    email: Optional[str] = None
    monthly_cost: Optional[float] = 0.0
    yearly_cost: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    billing_cycle: Optional[str] = "monthly"
    status: Optional[str] = "active"
    cancel_url: Optional[str] = None
    notes: Optional[str] = None
    next_billing_date: Optional[datetime] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    company: Optional[str] = None
    service_name: Optional[str] = None
    email: Optional[str] = None
    monthly_cost: Optional[float] = None
    yearly_cost: Optional[float] = None
    currency: Optional[str] = None
    billing_cycle: Optional[str] = None
    status: Optional[str] = None
    cancel_url: Optional[str] = None
    notes: Optional[str] = None
    next_billing_date: Optional[datetime] = None

class SubscriptionResponse(SubscriptionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

