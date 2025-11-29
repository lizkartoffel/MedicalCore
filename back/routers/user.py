from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from models.user import User, UserRead, UserUpdate
from core.dependencies import require_any_role
from core.security import get_current_user
from db.session import get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    session: Session = Depends(get_session),
    authorized_user: User = require_any_role(["distributor"])  # FIXED
):
    user_to_update = session.get(User, user_id)

    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.dict(exclude_unset=True)  # FIX for SQLModel/Pydantic v1

    for key, value in update_data.items():
        setattr(user_to_update, key, value)

    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)

    return user_to_update

@router.get("/", response_model=List[UserRead])
async def read_all_users(
    session: Session = Depends(get_session),
    authorized_user: User = require_any_role(["distributor"])
):
    return session.exec(select(User)).all()


# """this module handles user profile updates and retrieval using Supabase."""


# # def update_premium_status(user: User):
# #     """Automatically set premium if user is a distributor with active subscription."""
# #     if user.role == "distributor" and user.subscription_active:
# #         user.is_premium = True
# #     else:
# #         user.is_premium = False
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlmodel import Session, select
# from typing import List

# # Assuming the import path for the models and dependencies
# from models.user import User, UserRead, UserUpdate 
# from core.dependencies import require_any_role 
# # NOTE: Assuming get_current_user is also in core/security.py
# from core.security import get_current_user 
# from db.session import get_session # NOTE: Assuming db.session exists

# router = APIRouter(prefix="/users", tags=["users"])


# @router.get("/me", response_model=UserRead)
# async def read_user_me(current_user: User = Depends(get_current_user)):
#     """Get the profile of the current authenticated user."""
#     # User is retrieved by get_current_user, which is implicitly authorized by JWT
#     return current_user


# @router.put("/{user_id}", response_model=UserRead)
# async def update_user(
#     user_id: str, 
#     user_data: UserUpdate, 
#     session: Session = Depends(get_session),
#     # RBAC protection: Only "distributor" users can update other users (or an "admin" if you add that role)
#     authorized_user: User = Depends(require_any_role(["distributor"])) 
# ):
#     """
#     Update a user's details. Requires the 'distributor' role to execute.
#     This includes the ability to update the target user's 'roles' list.
#     """
#     user_to_update = session.get(User, user_id)
    
#     if not user_to_update:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     # This handles merging the Optional fields from UserUpdate
#     update_data = user_data.model_dump(exclude_unset=True)
    
#     # Apply updates
#     for key, value in update_data.items():
#         setattr(user_to_update, key, value)

#     session.add(user_to_update)
#     session.commit()
#     session.refresh(user_to_update)
    
#     return user_to_update


# @router.get("/", response_model=List[UserRead])
# async def read_all_users(
#     session: Session = Depends(get_session),
#     # RBAC protection: Only users with the 'distributor' role can view the full list
#     authorized_user: User = Depends(require_any_role(["distributor"]))
# ):
#     """Retrieve a list of all users. Protected by RBAC dependency."""
#     users = session.exec(select(User)).all()
#     return users