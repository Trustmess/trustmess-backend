from fastapi import APIRouter
from src.db import queries

router = APIRouter()


# ! DEV ROUTE
# ! ONLY DEV, DELETE BEFORE DEPLOY
# ! Get All users with passwords
# ! *****************************************************************************
@router.get(
    "/dev/users_with_pass/",
    name="Read Users with pass",
    tags=["dev"],
    description="Don't use on prod",
)
async def get_all_users_with_pass():
    users = queries.get_all_users_with_pass()
    return [dict(user) for user in users]


# ! *****************************************************************************
