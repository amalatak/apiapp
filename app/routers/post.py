from .. import models, schemas, oath2
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import engine, SessionLocal, get_db

# TBD on why we do this
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oath2.get_current_user),
        limit: int = 10, skip: int = 0, search: Optional[str]=""):
    # ^^^^ limit is a query parameter** see notes 
    # If we wanted to filter posts by owner
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # SqlAlchemy join defaults to left, inner join
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id)\
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def creat_post(post: schemas.CreatePost, db: Session = Depends(get_db), 
        current_user : int = Depends(oath2.get_current_user)):

     # ** operator unpacks the post input into usable format so that not all fields have to be typed out
     # Also add foreign key
    new_post = models.Post(owner_id=current_user.id, **post.dict() )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db), 
        current_user : int = Depends(oath2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id)\
        .filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} was not found')

    return post

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), 
        current_user : int = Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} was not found')
    # Make sure user only deletes his own posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), 
        current_user : int = Depends(oath2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} was not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()