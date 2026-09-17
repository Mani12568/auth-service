from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from database import engine, get_session
from models import User, SQLModel
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post("/signup")
def signup(email: str, password: str, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=email, hashed_password=hash_password(password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}


@app.post("/login")
@limiter.limit("5/minute")
def login(request: Request, email: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = decode_token(token)

    if payload is None or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    email = payload.get("sub")
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "email": user.email, "created_at": user.created_at}