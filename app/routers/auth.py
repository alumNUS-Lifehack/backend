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

@router.post("/register")
async def register(user: schemas.UserRegister):
    '''
    Description
    ===========
        Registers a new user.
        If a user is a mentor, a group is created for them.
    
    Parameters
    ==========
        email:     NUSNet email address
        name:      Full name (in titlecase)
        linkedin:  LinkedIn profile URL
        headline:  Job title/School/Course/Tech Stack etc.
        gradyear:  Graduation year
        course:    Course of study
        is_mentor: True if user is a mentor, False if user is a mentee

    Returns
    =======
        Success message if user is registered successfully; error message otherwise.
    '''
    if user.email is None or user.password is None:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        auth_done, usr_ref_done, grp_ref_done = False, False, False
        new_user = auth.create_user(
           email=user.email,
           password=user.password
        )
        auth_done = True
        usr_ref = firestore_client.collection("users")
        usr_ref.document(user.email[:8]).set({
                "uid": user.email[:8],
                "name": user.name,
                "linkedin": user.linkedin,
                "headline": user.headline,
                "gradyear": user.gradyear,
                "course": user.course,
                "is_mentor": user.is_mentor,
                "assigned_mentor": ""
            })
        usr_ref_done = True
        # create group if mentor
        if user.is_mentor:
            grp_ref = firestore_client.collection("groups")
            grp_ref.document(user.email[:8]).set({
                "gid": user.email[:8],
                "mentees": []
            })
            grp_ref_done = True
            # create chat with welcome message for mentees
            chat_ref = grp_ref.document(user.email[:8]).collection("messages")
            first_message: schemas.Message = {
                "createdAt": firestore.SERVER_TIMESTAMP,
                "sentBy": user.email[:8],
                "text": f"Welcome to your chat with {user.name}! Feel free to introduce yourself and ask any questions you have about {user.course} or general career advice."
            }
            chat_ref.add(first_message)
        return JSONResponse(content={'message': f'Successfully created user {new_user.uid}'}, status_code=200)    
    except Exception as e:
        print(e)
        # guard against partial creation
        if auth_done: auth.delete_user(user.email[:8])
        if usr_ref_done: usr_ref.document(user.email[:8]).delete()
        if grp_ref_done: grp_ref.document(user.email[:8]).delete()
        return HTTPException(detail={'message': 'Error Creating User'}, status_code=400)

@router.post("/login")
async def login(user: schemas.UserLogin):
    '''
    Description
    ===========
        Logs a user in.

    Parameters
    ==========
        email:     NUSNet email address
        password:  Password

    Returns
    =======
        JWT token if user is logged in successfully; error message otherwise.
    '''
    try:
        logged_in_user = pb.auth().sign_in_with_email_and_password(user.email, user.password)
        jwt = logged_in_user['idToken']
        user = firestore_client.collection("users").document(user.email[:8]).get().to_dict()
        return JSONResponse(content={'token': jwt, 'user': user}, status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)

@router.post("/ping")
async def validate(request: Request):
    '''
    Description
    ===========
        Validates a JWT token.

    Parameters
    ==========
        Authorization header: JWT token

    Returns
    =======
        User ID if token is valid; error message otherwise.
    '''
    try:
        headers = request.headers
        jwt = headers.get('authorization')
        # print(f"jwt:{jwt}")
        user = auth.verify_id_token(jwt)
        return user["uid"]
    except:
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)