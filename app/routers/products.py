from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_user
import schema, models

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)
# create a new product 
@router.post("/", response_model=schema.ProductOut)
async def add_product(product: schema.CreateProduct,db: Session = Depends(get_db),current_user: dict = Depends(verify_user)):
    categories = db.query(models.Category).filter(models.Category.id.in_(product.category_ids)).all()   
    if not categories:
        raise HTTPException(status_code=404, detail="Invalid category IDs")    
  
    new_product = models.Product(
        name=product.name,
        price=product.price,
        stock=product.stock,
        categories=categories
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# view all user products
@router.get("/", response_model=list[schema.ProductOut])
async def view_products(
    current_user: dict = Depends(verify_user),
    db: Session = Depends(get_db)
):
    products = db.query(models.Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No product found.")
    return products

# view a user product by id
@router.get("/{id}", response_model=schema.ProductOut)
async def get_product_by_id(
    id: int,current_user: dict = Depends(verify_user),db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# update a user product by id 
@router.put("/{id}", response_model=schema.ProductOut)
async def update_product(id: int,product_data: schema.UpdateProduct,current_user: dict = Depends(verify_user),db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = product_data.name
    product.price = product_data.price
    product.stock = product_data.stock

    categories = db.query(models.Category).filter(models.Category.id.in_(product_data.category_ids)).all()
    product.categories = categories

    db.commit()
    db.refresh(product)
    return product

#delete a prudct by id 
@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    current_user: dict = Depends(verify_user),
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    order_item_exists = db.query(models.OrderItem).filter(models.OrderItem.product_id == product_id).first()
    if order_item_exists:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product because it has been used in an order."
        )
    db.delete(product)
    db.commit()
    return {"message": f"Product with ID {product_id} deleted successfully"}