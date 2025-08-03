from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

class CommissionInstallment(Base):
    __tablename__ = "commission_installments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)
    installment_number = Column(Integer, nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    projected_payment_date = Column(Date, nullable=False)
    status = Column(String(20), default="Projected") # Ex: 'Projected', 'Paid', 'Canceled'
    paid_date = Column(Date, nullable=True)
    paid_amount = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        {'unique_together': ('sale_id', 'installment_number')},
    )


