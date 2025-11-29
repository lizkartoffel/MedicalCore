from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from db.session import create_db_and_tables
from routers.auth import router as auth_router
from routers.product import router as product_router
from routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup: Create database tables
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")
    yield
    # Shutdown: Add cleanup code here if needed
    print("Shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="MedSite API",
    description="API for MedSite platform",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to MedSite API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}