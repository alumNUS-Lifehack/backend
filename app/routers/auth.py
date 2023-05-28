from fastapi import FastAPI, Depends, APIRouter, HTTPException, Header, Request
from fastapi.responses import JSONResponse
import passlib
from passlib.hash import pbkdf2_sha256
import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth, firestore

from app import schemas

cred = credentials.Certificate('alumnus_service_account_keys.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase_config.json')))
firestore_client = firestore.client()

router = APIRouter(
    prefix="/v1/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", include_in_schema=False)
async def register(user: schemas.UserRegister):
    if user.email is None or user.password is None:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        new_user = auth.create_user(
           email=user.email,
           password=user.password
        )
        usr_ref = firestore_client.collection("users")
        usr_ref.document(user.email[:8]).set({
                "uid": user.email[:8],
                "name": user.name,
                "linkedin": user.linkedin,
                "headline": user.headline,
                "gradyear": user.gradyear,
                "course": user.course,
                "is_mentor": user.is_mentor
            })
        return JSONResponse(content={'message': f'Successfully created user {new_user.uid}'}, status_code=200)    
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'Error Creating User'}, status_code=400)

@router.post("/login", include_in_schema=False)
async def login(user: schemas.UserLogin):
    try:
        logged_in_user = pb.auth().sign_in_with_email_and_password(user.email, user.password)
        jwt = logged_in_user['idToken']
        return JSONResponse(content={'token': jwt}, status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)

@router.post("/ping", include_in_schema=False)
async def validate(request: Request):
    try:
        headers = request.headers
        jwt = headers.get('authorization')
        # print(f"jwt:{jwt}")
        user = auth.verify_id_token(jwt)
        return user["uid"]
    except:
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)