from pydantic import BaseModel
from src.models import Role
from typing import List

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Roles(BaseModel):
    name: str

class PermissionCreate(BaseModel):
    name: str