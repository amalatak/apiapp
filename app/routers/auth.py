from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oath2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_cridentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # Query the database for users whos email are equal to the email provided
    # OAuth2PasswordRequestForm requires that user cridentials be passed in as form-data
    user = db.query(models.User).filter(models.User.email == user_cridentials.username).first()

    # Validate cridentials
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid cridentials")
    if not utils.verify(user_cridentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Cridentials")

    # Create token
    access_token = oath2.create_access_token(data={"user_id" : user.id})

    return {"access_token" : access_token, "token_type" : "bearer"}




