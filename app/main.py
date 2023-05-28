from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import schemas
from app.routers import auth, users

description = """
AlumNUS is a platform for NUS students to connect with and receive mentorship from NUS alumni.
This API is used to authenticate users and retrieve user data.
"""

app: FastAPI = FastAPI(
    title="AlumNUS API",
    description=description,
    version="0.1.0"
)

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

app.include_router(auth.router)
app.include_router(users.router)
