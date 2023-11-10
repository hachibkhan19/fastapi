from fastapi import FastAPI, status
from . import models
from .database import engine
from . routes import blogRouter, userRouter, authRouter
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

## bitfumes fastapi 1:20


@app.get("/", status_code=status.HTTP_200_OK)
def index():
    return{
        "test": "Health is ok"
    }

app.include_router(blogRouter)
app.include_router(userRouter)
app.include_router(authRouter)