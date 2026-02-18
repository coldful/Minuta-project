from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Dict
from uuid import uuid4

app = FastAPI(title="Minuta API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users: Dict[str, dict] = {}

class UserDisplay(BaseModel):
    id: str
    email: EmailStr

class UserInsert(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length= 128)
    password_confirm: str = Field(min_length=6, max_length= 128)

@app.get("/users", response_model= list[UserDisplay])
def list_users():
    return [{"id": user["id"], "email": user["email"]} for user in users.values()]

@app.post("/auth/register", response_model= UserDisplay, status_code= 201)
def register(payload: UserInsert):
    email = payload.email.lower()

    if payload.password != payload.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if email in users:
        raise HTTPException(status_code=409, detail="Email already registered")

    # ВАЖНО: пока без базы и без хеширования (позже исправим)
    user_id = str(uuid4())
    users[email] = {"id": user_id, "email": email, "password": payload.password}

    return {"id": user_id, "email": email}