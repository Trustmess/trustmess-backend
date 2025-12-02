from fastapi import APIRouter
from src.db import queries

router = APIRouter()


# * Get all users
# *****************************************************************************
@router.get("/users/", name="Get All Users", tags=["database"])
async def get_all_users():
    users = queries.get_all_users()
    return [dict(user) for user in users]


# *****************************************************************************
