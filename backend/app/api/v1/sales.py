from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.crud import sale as crud_sale
from app.schemas.sale import Sale, SaleCreate, SaleUpdate
from app.schemas.user import User
from app.api.v1.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[Sale])
async def read_sales(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role in ["Gestor", "Supervisor"]:
        sales = await crud_sale.get_sales(db, skip=skip, limit=limit)
    else:
        sales = await crud_sale.get_sales_by_user(db, user_id=str(current_user.id), skip=skip, limit=limit)
    return sales

@router.post("/", response_model=Sale)
async def create_sale(
    sale: SaleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await crud_sale.create_sale(db=db, sale=sale, user_id=str(current_user.id))

@router.get("/{sale_id}", response_model=Sale)
async def read_sale(
    sale_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_sale = await crud_sale.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Verificar se o usuário tem permissão para ver esta venda
    if current_user.role not in ["Gestor", "Supervisor"] and str(db_sale.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return db_sale

@router.put("/{sale_id}", response_model=Sale)
async def update_sale(
    sale_id: str,
    sale_update: SaleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_sale = await crud_sale.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Verificar se o usuário tem permissão para editar esta venda
    if current_user.role not in ["Gestor", "Supervisor"] and str(db_sale.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return await crud_sale.update_sale(db=db, sale_id=sale_id, sale_update=sale_update)

@router.delete("/{sale_id}")
async def delete_sale(
    sale_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_sale = await crud_sale.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Verificar se o usuário tem permissão para deletar esta venda
    if current_user.role not in ["Gestor", "Supervisor"] and str(db_sale.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = await crud_sale.delete_sale(db=db, sale_id=sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    return {"message": "Sale deleted successfully"}

