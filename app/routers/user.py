from .. import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import engine, SessionLocal, get_db

# TBD on why we do this
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password - user.password

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User( **user.dict() )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    # Get a single user

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {id} not found")
    
    return user

