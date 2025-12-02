# seed_db.py
import os
import sys
from sqlmodel import Session, select, SQLModel
from typing import List, Dict, Any

# Ensure project root is in the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- IMPORTANT IMPORTS ---
# Ensure these imports match your actual file structure
from models.user import User, UserRole 
from db.session import engine 
from core.security import get_password_hash 

# --- Seed Data Definitions (Using short, safe passwords) ---
SEED_USERS: List[Dict[str, Any]] = [
    {
        # Admin User
        "username": "admin_user",
        "email": "admin@medcore.com",
        "password": "adminpass1", # SHORTENED PASSWORD
        "full_name": "System Admin",
        "is_premium": True,
        "role": UserRole.ADMIN, 
        "roles": [UserRole.ADMIN.value, UserRole.DISTRIBUTOR.value, UserRole.CUSTOMER.value],
    },
    {
        # Distributor User
        "username": "distributor_a",
        "email": "distributor@medcore.com",
        "password": "distpass1", # SHORTENED PASSWORD
        "full_name": "Alpha Medical Supply",
        "is_premium": False,
        "role": UserRole.DISTRIBUTOR,
        "roles": [UserRole.DISTRIBUTOR.value],
    },
    {
        # Customer User
        "username": "customer_b",
        "email": "customer@medcore.com",
        "password": "custpass1", # SHORTENED PASSWORD
        "full_name": "Dr. Ben Customer",
        "is_premium": True,
        "role": UserRole.CUSTOMER,
        "roles": [UserRole.CUSTOMER.value],
    },
]

def seed_users():
    """Initializes the database with predefined users if they don't exist."""
    print("🎬 Starting user database seeding...")
    
    with Session(engine) as session:
        for user_data in SEED_USERS:
            email = user_data["email"]
            # Check if user already exists by email
            existing_user = session.exec(
                select(User).where(User.email == email)
            ).first()
            
            if existing_user:
                print(f"✅ User {email} already exists. Skipping.")
                continue

            # 1. Pop the plain password and hash it
            plain_password = user_data.pop("password")
            hashed_password = get_password_hash(plain_password)
            
            # 2. Create the new User object
            new_user = User(
                **user_data,
                hashed_password=hashed_password,
                is_active=True,
                subscription_active=False
            )
            
            session.add(new_user)
            print(f"➕ Adding user: {new_user.email} with primary role {new_user.role.value}")

        try:
            session.commit()
            print("🎉 Database seeding complete. All new users committed.")
        except Exception as e:
            session.rollback()
            # If the error is related to database access (file lock, missing column), it often happens here.
            print(f"❌ Error during database commit: {e}")

if __name__ == "__main__":
    # Ensure all models are imported so SQLModel knows about them (CRUCIAL for metadata)
    from models.user import User 
    
    # CRUCIAL FIX: Create all tables based on current model definitions
    print("🔄 Checking database schema and creating tables...")
    SQLModel.metadata.create_all(engine) 
    print("✅ Tables created/verified.")

    seed_users()