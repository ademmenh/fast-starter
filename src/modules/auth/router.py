from fastapi import APIRouter
from .controller import register, login

authRouter = APIRouter()
authRouter.add_api_route('/register', register, methods=['GET'])
authRouter.add_api_route('/login', login, methods=['GET'])
