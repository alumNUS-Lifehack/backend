from fastapi import FastAPI, Depends, APIRouter, HTTPException, Header, Request
from fastapi.responses import JSONResponse
import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth, firestore
from typing import Annotated
import re

from app import schemas

cred = credentials.Certificate('alumnus_service_account_keys.json')
from app.routers.auth import firebase
pb = pyrebase.initialize_app(json.load(open('firebase_config.json')))
firestore_client = firestore.client()

router = APIRouter(
    prefix="/v1/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/mentor/{uid}")
async def get_mentor(uid: str, request: Request):
    try:
        headers = request.headers
        token = headers['authorization']
        decoded_token = auth.verify_id_token(token)
        usr_ref = firestore_client.collection("users")
        usr = usr_ref.document(uid).get()
        if usr.exists:
            if usr.to_dict()['is_mentor']:
                mentor = usr_ref.document(uid).get().to_dict()
                return JSONResponse(content=mentor, status_code=200)
            else:
                return HTTPException(detail={'message': 'User is not a mentor'}, status_code=400)
        else:
            return HTTPException(detail={'message': 'User does not exist'}, status_code=400)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'Error getting mentor'}, status_code=400)

@router.get("/mentee/{uid}")
async def get_mentee(uid: str, request: Request):
    try:
        headers = request.headers
        token = headers['authorization']
        decoded_token = auth.verify_id_token(token)
        usr_ref = firestore_client.collection("users")
        usr = usr_ref.document(uid).get()
        if usr.exists:
            if not usr.to_dict()['is_mentor']:
                mentee = usr_ref.document(uid).get().to_dict()
                return JSONResponse(content=mentee, status_code=200)
            else:
                return HTTPException(detail={'message': 'User is not a mentee'}, status_code=400)
        else:
            return HTTPException(detail={'message': 'User does not exist'}, status_code=400)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'Error getting mentee'}, status_code=400)

@router.get("/all_mentors")
async def get_all_mentors(request: Request):
    try:
        headers = request.headers
        token = headers['authorization']
        decoded_token = auth.verify_id_token(token)
        usr_ref = firestore_client.collection("users")
        all_users = usr_ref.stream()
        mentors = []
        for user in all_users:
            if user.to_dict()['is_mentor']:
                mentors.append(user.to_dict())
        return JSONResponse(content=mentors, status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(detail={'message': 'Error getting mentors'}, status_code=400)