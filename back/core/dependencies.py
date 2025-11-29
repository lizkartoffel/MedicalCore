# from fastapi import Depends, HTTPException  
# from models.user import User
# from core.security import get_current_user

# def require_role(role: str):
#     def role_checker(user: User = Depends(get_current_user)):
#         if user.role != role:
#             raise HTTPException(status_code=403, detail=f"Only {role}s can perform this action.")
#         return user
#     return Depends(role_checker)
from fastapi import Depends, HTTPException, status
from typing import List

# Import the User model from where it is defined
from models.user import User 

# Import the dependency function from the security file (where get_current_user lives)
# NOTE: You'll need to define core/security.py or move get_current_user here
from core.security import get_current_user


def require_any_role(required_roles: List[str]):
    """
    Dependency factory to check if the current user has at least one of the 
    required roles listed in their user.roles field (List[str]).
    
    Usage Example: 
    @router.get("/admin", dependencies=[Depends(require_any_role(["distributor", "admin"]))])
    """
    def role_checker(user: User = Depends(get_current_user)):
        # Convert user's roles to a set for fast lookup
        user_roles_set = set(user.roles)
        required_roles_set = set(required_roles)
        
        # Check for intersection between required roles and user's roles
        # If the intersection is empty, the user does not have any of the required roles.
        if not user_roles_set.intersection(required_roles_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Access denied. Required roles: {', '.join(required_roles)}."
            )
        return user
        
    # Returns the dependency object
    return Depends(role_checker)


def require_single_role(role_name: str):
    """
    Dependency factory to check if the current user's primary role 
    matches the required role (str). (Less flexible than require_any_role).
    """
    def role_checker(user: User = Depends(get_current_user)):
        # Checks the single 'role' Enum field (converted to string value for comparison)
        if user.role.value != role_name: 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"Only {role_name}s can perform this action.")
        return user
    return Depends(role_checker)