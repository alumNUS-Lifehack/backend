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
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase_config.json')))
firestore_client = firestore.client()

router = APIRouter(
    prefix="/v1/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)