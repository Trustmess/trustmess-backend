from pydantic import BaseModel


class DeleteUserRequest(BaseModel):
    username: str


class UpdateUsernameRequest(BaseModel):
    current_username: str
    new_username: str


class UpdatePasswordRequest(BaseModel):
    username: str
    new_password: str
