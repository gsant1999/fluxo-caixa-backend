from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

class PaymentFlow(Base):
    __tablename__ = "payment_flows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operator_name = Column(String(100), unique=True, nullable=False)
    flow_type = Column(String(50), nullable=False) # Ex: 'DELAYED_MONTHLY', 'NEXT_MONTH'
    delay_days = Column(Integer, default=0)
    payment_days = Column(JSONB) # Array JSON de dias do mês [15, 30]
    payment_day = Column(Integer) # Dia específico do mês (para NEXT_MONTH)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


