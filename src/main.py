from fastapi import FastAPI
from src.routers import auth, roles, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Auth System"}
