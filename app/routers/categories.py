from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_user
from database import get_db
import schema, models
from typing import List

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# Create a new category 
@router.post("/", response_model=schema.CategoryOut)
async def create_category(category:schema.CategoryCreate, db:Session=Depends(get_db),current_user: dict = Depends(verify_user)):

    newCategory = models.Category(
        name = category.name,
        description = category.description
    )
    db.add(newCategory)
    db.commit()
    db.refresh(newCategory)
    return newCategory

# View all categories
@router.get("/", response_model=List[schema.CategoryOut])
async def view_categories(current_user:dict = Depends(verify_user),db: Session = Depends(get_db)):
    all_categories = db.query(models.Category).all()
    if not all_categories:
        raise HTTPException(status_code=404, detail="No Category was not found")
    return all_categories

# View a category by its id
@router.get("/{category_id}", response_model=schema.CategoryOut)
def get_category_by_id(category_id: int,current_user:dict = Depends(verify_user), db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# update a category by its id 
@router.put("/{category_id}", response_model=schema.CategoryOut)
async def update_category(category_id: int, updated_data: schema.CategoryCreate,current_user:dict = Depends(verify_user), db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = updated_data.name
    category.description = updated_data.description
    db.commit()
    db.refresh(category)
    return category

# delete a category by its id
@router.delete("/{category_id}")
async def delete_category(category_id: int,current_user:dict = Depends(verify_user), db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return {"message": f"Category with ID {category_id} deleted successfully"}





