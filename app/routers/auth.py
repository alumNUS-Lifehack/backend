from fastapi import FastAPI, Depends, HTTPException, APIRouter

from app import schemas

router = APIRouter(
    prefix="/v1/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

save = None

@router.post("/login")
async def login(user: schemas.UserLogin):
    hashed = pbkdf2_sha256.hash(user.password)
    status = pbkdf2_sha256.verify(user.password, save)
    return {"username": user.username, "status": status }

@router.post("/register")
async def register(user: schemas.UserLogin):
    hashed = pbkdf2_sha256.hash(user.password)
    global save
    save = hashed
    status = pbkdf2_sha256.verify(user.password, save)
    return {"username": user.username, "status": status}
