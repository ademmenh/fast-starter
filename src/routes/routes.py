from fastapi import FastAPI, APIRouter
from src.modules.auth import authRouter

def addRoutes (app: FastAPI):
    app.include_router(authRouter, prefix="/auth", tags=["Auth"])
