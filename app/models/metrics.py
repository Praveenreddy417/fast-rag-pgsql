from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class TicketMetrics(Base):
    __tablename__ = "ticket_metrics"

    id = Column(Integer, primary_key=True)
    confidence = Column(Float)
    tier = Column(String)
    severity = Column(String)
    needs_escalation = Column(Boolean)
    guardrail_blocked = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
