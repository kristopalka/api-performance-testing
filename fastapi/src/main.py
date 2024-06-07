import random

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from .database import get_message_by_id, get_db
from .fibonacci import generate_fibonacci

app = FastAPI(
    docs_url=None,
    redoc_url=None
)


@app.get("/hello", summary="Returns simple JSON object with 'Hello World!' text", response_model=dict)
async def hello():
    return {"message": "Hello World!"}


@app.get("/fibonacci/{n}", summary="Returns n-th element of Fibonacci Sequence in a JSON object", response_model=dict)
async def fibonacci(n: int):
    if n < 0:
        raise HTTPException(status_code=400, detail="Parameter n must be a non-negative integer")

    return {"number": n, "value": generate_fibonacci(n)}


@app.get("/database", summary="Returns random element from database", response_model=dict)
async def database(db: Session = Depends(get_db)):
    random_id = random.randint(1, 25)
    message = get_message_by_id(db, random_id)

    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    return {"message": message.val}
