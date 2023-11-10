from fastapi import status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas, hashing
from . database import get_db


## blog repository
def get_blog(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session):
    blog = models.Blog(name=request.name, description=request.description, published=request.published, user_id=1)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def get_single_blog(pk:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == pk).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {pk} is not found in database.')

    return blog


def update(pk:int, request: schemas.Blog,  db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == pk)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {pk} is not found in database.')
    blog.update({"name": request.name, "description": request.description, "published": request.published})
    db.commit()

def destroy(pk:int, db: Session):
    db.query(models.Blog).filter(models.Blog.id == pk).delete(synchronize_session=False)
    db.commit()


## user repository
def create_user(request: schemas.User, db: Session):
    user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(id:int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} is not found in database.')

    return user
