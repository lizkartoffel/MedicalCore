from fastapi import Depends, HTTPException  
from models.user import User
from core.security import get_current_user

def require_role(role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail=f"Only {role}s can perform this action.")
        return user
    return Depends(role_checker)