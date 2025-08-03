from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleUpdate

async def get_sale(db: AsyncSession, sale_id: str) -> Optional[Sale]:
    result = await db.execute(
        select(Sale).options(selectinload(Sale.user)).where(Sale.id == sale_id)
    )
    return result.scalar_one_or_none()

async def get_sales(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Sale]:
    result = await db.execute(
        select(Sale).options(selectinload(Sale.user)).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_sales_by_user(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[Sale]:
    result = await db.execute(
        select(Sale).options(selectinload(Sale.user))
        .where(Sale.user_id == user_id)
        .offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_sale(db: AsyncSession, sale: SaleCreate, user_id: str) -> Sale:
    db_sale = Sale(
        user_id=user_id,
        client_name=sale.client_name,
        operator_name=sale.operator_name,
        product_type=sale.product_type,
        lives=sale.lives,
        monthly_value=sale.monthly_value,
        sale_date=sale.sale_date,
        status=sale.status
    )
    db.add(db_sale)
    await db.commit()
    await db.refresh(db_sale)
    return db_sale

async def update_sale(db: AsyncSession, sale_id: str, sale_update: SaleUpdate) -> Optional[Sale]:
    db_sale = await get_sale(db, sale_id)
    if not db_sale:
        return None
    
    update_data = sale_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sale, field, value)
    
    await db.commit()
    await db.refresh(db_sale)
    return db_sale

async def delete_sale(db: AsyncSession, sale_id: str) -> bool:
    db_sale = await get_sale(db, sale_id)
    if not db_sale:
        return False
    
    await db.delete(db_sale)
    await db.commit()
    return True

