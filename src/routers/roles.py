from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from src.db_utils import get_db_session
from src.schemas import Roles, PermissionCreate
from src.models import Role, Permission
from .auth import get_user_id

router = APIRouter(prefix="/roles", tags=["roles"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/")
def create_role(role: Roles, db: Session = Depends(get_db_session), token: str = Depends(oauth2_scheme)):
    user = get_user_id(token)
    if not user.get("isadmin"):
        return {"message": "You are not authorized to create roles."}
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.post("/{role_id}/permissions")
def add_permission_to_role(role_id: int, permission:PermissionCreate, db: Session = Depends(get_db_session),token: str = Depends(oauth2_scheme)):
    user = get_user_id(token)
    if not user.get("isadmin"):
        return {"message": "You are not authorized to assign permissions to roles."}

    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db_permission = db.query(Permission).filter(Permission.name == permission.name).first()

    if not db_permission:
        db_permission =     Permission(name=permission.name)
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
    try:
        db_role.permissions.append(db_permission)
        db.commit()
        db.refresh(db_role)
    except Exception as e:
        return {"message": "Permission already assigned to role."}
    return db_role.permissions
