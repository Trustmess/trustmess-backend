from fastapi import APIRouter, HTTPException
from src.db import queries
from src.schemas.auth import AuthRequest
from src.secure.auth_middleware import get_current_user

router = APIRouter()

# ? ROOT ROUTE
# *****************************************************************************
@router.get("/")
async def read_root():
    return {
        "status": "Ok",
        "docs": "/docs",
        }
# *****************************************************************************


# * Get all users
# *****************************************************************************
@router.get("/users/", name="Get All Users", tags=["database"])
async def get_all_users():
    users = queries.get_all_users()
    return [dict(user) for user in users]
# *****************************************************************************

# ! DEV ROUTE
# ! ONLY DEV, DELETE BEFORE DEPLOY
# ! Get All users with passwords
# ! *****************************************************************************
@router.get("/dev/users_with_pass/", name="Read Users with pass", tags=["dev"], description="Don't use on prod")
async def get_all_users_with_pass():
    users = queries.get_all_users_with_pass()
    return [dict(user) for user in users]
# ! *****************************************************************************
