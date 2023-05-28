from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import passlib
from passlib.hash import pbkdf2_sha256

from app import schemas

app: FastAPI = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = None
save = None

@app.post("/login")
async def login(user: schemas.UserLogin):
    hashed = pbkdf2_sha256.hash(user.password)
    status = pbkdf2_sha256.verify(user.password, save)
    return {"username": user.username, "status": status }

@app.post("/register")
async def register(user: schemas.UserLogin):
    hashed = pbkdf2_sha256.hash(user.password)
    global save
    save = hashed
    status = pbkdf2_sha256.verify(user.password, save)
    return {"username": user.username, "status": status}