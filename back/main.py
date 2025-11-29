from fastapi import FastAPI
from db.session import get_session
from contextlib import asynccontextmanager
from routers.auth import router as auth_router
from routers.product import router as product_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db = get_session()
    #init_db.connect()
    # Startup code
    print("Starting up...")
    yield
    # Shutdown code
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(product_router)