from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User registration and login 
class CreateUser(BaseModel):
    username:str
    email: EmailStr
    password: str

class CreateUserOut(BaseModel):
    id: int
    username:str
    email: EmailStr

    class Config:
        orm_mode = True

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# Product
class CreateProduct(BaseModel):
    name: str
    price: float
    stock:float
    category_ids:List[int]

class CategoryInProduct(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class ProductOut(BaseModel):
    id: int
    name: str
    stock:float
    price: float
    categories: List[CategoryInProduct] = []
    class Config:
        orm_mode = True

# category
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryOut(CategoryCreate):
    id: int
    class Config:
        orm_mode = True

#update product 
class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock:float
    category_ids: Optional[List[int]] = None

# orders
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

    class Config:
        orm_mode = True

class OrderOut(OrderCreate):
    id: int
    status: str
    order_date:datetime
    items: List[OrderItemOut]

    class Config:
        orm_mode = True

class UpdateOrderStatus(BaseModel):
    status: str
