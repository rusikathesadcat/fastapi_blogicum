from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.domain.use_cases.user_use_case import UserUseCase
from app.core.security import create_access_token
from app.core.config import settings
from app.schemas import Token

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_user_use_case(db: Session = Depends(get_db)) -> UserUseCase:
    return UserUseCase(db)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: UserUseCase = Depends(get_user_use_case)
):
    user = use_case.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}