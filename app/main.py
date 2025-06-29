from fastapi import FastAPI
from database import create_all_tables
from routers import authentication,products, categories, orders 

app = FastAPI()
create_all_tables()  

app.include_router(authentication.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(orders.router)