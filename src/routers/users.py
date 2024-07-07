from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.db_utils import get_db_session
from src.config import REDIS_URL
from redis import Redis
from src.models import  User, Role, UserRole
from .auth import get_user_id
from src.schemas import Roles

redis = Redis.from_url(REDIS_URL)
router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
def get_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    user = get_user_id(token) 
    if(user.get("isadmin")):
        users = db.query(User).all()
        return users
    return {"message": "You are not authorized to view this resource."}


@router.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    user = get_user_id(token)
    current_user = db.query(User).filter(User.username == user.get("username")).first()
    return current_user

@router.post("/{user_id}/roles")
def assign_role_to_user(user_id: int, role:Roles, db: Session = Depends(get_db_session),token: str = Depends(oauth2_scheme)):

    current_user = get_user_id(token)
    if not current_user.get("isadmin"):
        return {"message": "You are not authorized to assign roles to users."}

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_role = db.query(Role).filter(Role.name == role.name).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    user_role = UserRole(user_id=user_id, role_id=db_role.id)
    try:
        db.add(user_role)
        db.commit()
    except Exception as e:
        return {"message": "Role already assigned to user."}
    return {"message": "Role assigned to user successfully."}
