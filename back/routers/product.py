from fastapi import APIRouter, Depends, HTTPException, status
from models.product import Product, ProductCreate
from models.user import User
from sqlmodel import Session

from db.session import get_session
from core.dependencies import require_role
from core.security import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/create")
def create_product(data: ProductCreate, user: User = require_role("distributor"), session: Session = Depends(get_session)):
    if user.role != "distributor":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only distributors can post products.")

    product = Product(**data.dict(), owner_id=user.id)
    session.add(product)
    session.commit()
    session.refresh(product)

    return {"message": "Product created successfully", "product": product}


@router.put("/{product_id}")
def update_product(product_id: str, data: ProductCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):

    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if user.role != "distributor" or product.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this product")

    for key, value in data.model_dump().items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)
    return {"message": "Product updated successfully", "product": product}


@router.delete("/{product_id}")
def delete_product( product_id: str, user: User = Depends(get_current_user), session: Session = Depends(get_session)):

    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if user.role != "distributor" or product.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")

    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}