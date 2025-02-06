from typing import Annotated, Union
from fastapi import FastAPI, Cookie, Header, Response, status

from src.middlewares.cors import configCORS
from src.types.user import User
from src.utils.db import init_db, close_db
from src.routes.routes import addRoutes

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

configCORS(app)

addRoutes(app)


@app.get("/")
async def home(
    response: Response,
    authentication: Annotated[str, Header()] = None,
    access_token: Annotated[str, Cookie()] = None,
    refresh_token: Annotated[str, Cookie()] = None,
) -> dict[str, str] | str | int:

    response.status_code = status.HTTP_201_CREATED
    return {"message": "Welcome Home"}
