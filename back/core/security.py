from fastapi.security import HTTPBearer
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from models.user import User
from sqlmodel import select, Session
from db.session import get_session, supabase
from fastapi.security import HTTPAuthorizationCredentials

router = APIRouter( prefix="/security", tags=["security"] )

security = HTTPBearer(auto_error=False) #responsible for extracting and validating the token from the request headers.


def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)):  # Extract token using HTTPBearer if user is authenticated
    """Get the current authenticated user based on the provided token.
    added anywhere in code to make sure to only work if the user is authenticated."""
    if not cred:
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = cred.credentials.strip().removeprefix("Bearer ").strip()
    response = supabase.auth.get_user(token)

    if not response or not response.user:
        raise HTTPException(status_code=401, detail="Invalid token")

    # get role from your local DB
    user = session.exec(select(User).where(User.email == response.user.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
