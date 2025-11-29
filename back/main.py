from fastapi import FastAPI
from db.session import create_db_and_tables
from contextlib import asynccontextmanager
from routers.auth import router as auth_router
from routers.product import router as product_router

from db.session import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # Create database tables at startup
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(product_router)