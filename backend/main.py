from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Dict
from uuid import uuid4
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends

SECRET_KEY = "PLACEHOLDER"
TOKEN_EXPIRE_TIME = timedelta(minutes=30)
ALG = "HS256"
PSWD_LEN = 128

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#JSON models
class UserDisplay(BaseModel):
    id: str
    email: EmailStr

class UserInsert(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length= PSWD_LEN)
    password_confirm: str = Field(min_length=6, max_length= PSWD_LEN)

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

#Hash functions to guard password
def hash_pswd(pswd: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(
        pswd.encode("utf-8"),
        salt
    )
    return hashed.decode("utf-8")

def verify_pswd(pswd: str, hpswd: str):
    return bcrypt.checkpw(
        pswd.encode("utf-8"),
        hpswd.encode("utf-8"),
    )

#JWT token creation
def create_jwt(data: dict, expire_d= TOKEN_EXPIRE_TIME):
    expire_time = datetime.utcnow() + expire_d
    user_data = data.copy()
    user_data.update({"exp":expire_time})
    return jwt.encode(user_data, SECRET_KEY, ALG)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALG)
        email = payload.get("sub")
        if not email:
            raise HTTPException(401, "Invalid authentification token")
    except JWTError:
        raise HTTPException(401, "Invalid authentification token")
    
    user = users.get(email)
    if not user:
        raise HTTPException(401, "User not found")
    return user

app = FastAPI(title="Minuta API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Temporary storage for users
users: Dict[str, dict] = {}

#Simple action decorated functions
@app.get("/users", response_model= list[UserDisplay])
def list_users():
    return [{"id": user["id"], "email": user["email"]} for user in users.values()]

@app.post("/auth/register", response_model= UserDisplay, status_code= 201)
def register(payload: UserInsert):
    email = payload.email.lower()

    if payload.password != payload.password_confirm:
        raise HTTPException(400, "Passwords do not match")
    
    if email in users:
        raise HTTPException(409, "Email already registered")

    pw_len = len(payload.password.encode("utf-8"))
    if pw_len > PSWD_LEN:
        raise HTTPException(400, "Password is too long")

    user_id = str(uuid4())
    password_hash = hash_pswd(payload.password)
    users[email] = {"id": user_id, "email": email, "password_hash": password_hash}

    return {"id": user_id, "email": email}

@app.post("/auth/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends()):
    email = form.username.lower()
    password = form.password

    user = users.get(email)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    
    if not verify_pswd(password, user["password_hash"]):
        raise HTTPException(401, "Invalid password")
    
    return {"access_token": create_jwt({"sub" : email}), "token_type": "bearer"}

@app.get("/me", response_model= UserDisplay)
def display_me(current_user: dict = Depends(get_current_user)):
    return {"id" : current_user["id"], "email" : current_user["email"]}