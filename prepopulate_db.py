from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from src.models import User, Role, Permission, UserRole, role_permission_table
from src.security import get_password_hash
from src.config import DATABASE_URL


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# create a new session
session = SessionLocal()

# create a user
hashed_password = get_password_hash('admin123')
user = User(username='test-admin', email='admin@example.com', hashed_password=hashed_password, is_active=True, is_admin=True)

# add and commit the user to the database
session.add(user)
session.commit()

# close the session
session.close()
