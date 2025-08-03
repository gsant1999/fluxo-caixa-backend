from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db.database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    client_name = Column(String(255), nullable=False)
    operator_name = Column(String(100), nullable=False)
    product_type = Column(String(50), nullable=False)
    lives = Column(Integer, nullable=False)
    monthly_value = Column(Numeric(10, 2), nullable=False)
    sale_date = Column(Date, nullable=False)
    status = Column(String(50), default="Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamento com User
    user = relationship("User", back_populates="sales")

