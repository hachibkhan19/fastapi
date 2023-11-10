from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from . database import get_db
from . import repository
from .hashing import Hash
from .token import create_access_token
from .oauth2 import get_current_user

## blog router
blogRouter = APIRouter(prefix="/blog", tags=["blogs"])

@blogRouter.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_blog(db: Session = Depends(get_db), current_user:schemas.User = Depends(get_current_user)):
    return repository.get_blog(db)



@blogRouter.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return repository.create(request, db)


@blogRouter.get('/{pk}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_single_blog(pk, db: Session = Depends(get_db)):
    return repository.get_single_blog(pk, db)


@blogRouter.put('/{pk}', status_code=status.HTTP_202_ACCEPTED)
def update(pk, request: schemas.Blog,  db: Session = Depends(get_db)):
    return repository.update(pk, request, db)


@blogRouter.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(pk, db: Session = Depends(get_db)):
    return repository.destroy(pk, db)


## user router
userRouter = APIRouter(prefix="/user", tags=["users"])

@userRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session= Depends(get_db)):
    return repository.create_user(request, db)


@userRouter.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(get_db)):
    return repository.get_user(id, db)


## authentication router
authRouter = APIRouter(prefix="/login", tags=["authentication"])
@authRouter.post("/", status_code=status.HTTP_200_OK)
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    if not Hash.verify_password(user.password, request.password):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")
    
    
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    