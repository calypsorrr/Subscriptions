from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False, index=True)
    service_name = Column(String)
    email = Column(String)
    monthly_cost = Column(Float, default=0.0)
    yearly_cost = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    billing_cycle = Column(String, default="monthly")  # monthly, yearly, quarterly
    status = Column(String, default="active")  # active, cancelled, expired
    cancel_url = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    next_billing_date = Column(DateTime(timezone=True))

