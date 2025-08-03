from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

class CommissionRule(Base):
    __tablename__ = "commission_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operator_name = Column(String(100), nullable=False)
    product_type = Column(String(50), nullable=False)
    lives_min = Column(Integer, nullable=False)
    lives_max = Column(Integer, nullable=False)
    total_commission_multiplier = Column(Numeric(5, 2), nullable=False) # Ex: 2.00 para 200%
    installment_percentages = Column(JSONB, nullable=False) # Array JSON de percentuais [1.00, 0.50, 0.50]
    recurring_commission_multiplier = Column(Numeric(5, 4), default=0.0000) # Ex: 0.005 para 0.5% recorrente
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        {'unique_together': ('operator_name', 'product_type', 'lives_min', 'lives_max')},
    )


