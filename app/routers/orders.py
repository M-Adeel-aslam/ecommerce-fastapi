from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session
from database import *
from datetime import datetime
from auth import verify_user
from database import get_db
import schema, models


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)
# create a new order

@router.post("/", response_model=schema.OrderOut)
def create_order(order: schema.OrderCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_user)):

    new_order = models.Order(
        user_id=current_user["id"],
        status="Pending",
        order_date=datetime.utcnow()
    )
    db.add(new_order)
    db.commit()

    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found.")
        
        order_item = models.OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)

    return new_order

# View all orders
@router.get("/", response_model=List[schema.OrderOut])
def view_orders(db: Session = Depends(get_db),current_user: dict = Depends(verify_user)):
    orders = db.query(models.Order).filter(models.Order.user_id == current_user["id"]).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No user order found.")
    return orders

#View a order by its id 
@router.get("/{order_id}", response_model=schema.OrderOut)
def get_order_by_id(
    order_id: int,db: Session = Depends(get_db),current_user: dict = Depends(verify_user)):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user["id"]
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# update a order by its id
@router.put("/{order_id}", response_model=schema.OrderOut)
def update_order_status(order_id: int,status_update: schema.UpdateOrderStatus,db: Session = Depends(get_db),current_user: dict = Depends(verify_user)):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user["id"]
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order
# delete a order by its id
@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_user)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user["id"]
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": f"Order {order_id} deleted successfully."}